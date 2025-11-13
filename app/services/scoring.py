"""
Servicio de Scoring - Sistema de puntos comerciales
"""
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Cliente, ActividadComercial
from app.core.config import settings


def registrar_actividad(
    db: Session,
    cliente_id: str,
    tipo_actividad: str,
    descripcion: str = None,
    metadata_json: str = None,
    agente_id: str = None
) -> ActividadComercial:
    """
    Registrar actividad comercial y otorgar puntos
    """
    # Mapear tipo de actividad a puntos
    puntos_map = {
        'login': Decimal(str(settings.PUNTOS_LOGIN)),
        'ver_poliza': Decimal(str(settings.PUNTOS_VER_POLIZA)),
        'descargar_pdf': Decimal(str(settings.PUNTOS_DESCARGAR_PDF)),
        'solicitar_cotizacion': Decimal(str(settings.PUNTOS_SOLICITAR_COTIZACION)),
        'llamado_nuevo': Decimal(str(settings.PUNTOS_LLAMADO_NUEVO)),
        'llamado_seguimiento': Decimal(str(settings.PUNTOS_LLAMADO_SEGUIMIENTO)),
        'cotizado': Decimal(str(settings.PUNTOS_COTIZADO)),
        'propuesta_entregada': Decimal(str(settings.PUNTOS_PROPUESTA_ENTREGADA)),
        'cliente_cerrado': Decimal(str(settings.PUNTOS_CLIENTE_CERRADO)),
        'cliente_perdido': Decimal(str(settings.PUNTOS_CLIENTE_PERDIDO)),
    }
    
    puntos = puntos_map.get(tipo_actividad, Decimal('0'))
    
    # Crear actividad
    actividad = ActividadComercial(
        cliente_id=cliente_id,
        agente_id=agente_id,
        tipo_actividad=tipo_actividad,
        puntos_otorgados=puntos,
        descripcion=descripcion,
        metadata_json=metadata_json
    )
    
    db.add(actividad)
    
    # Actualizar score del cliente
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if cliente:
        cliente.score_comercial += int(puntos)
    
    db.commit()
    db.refresh(actividad)
    
    return actividad


def obtener_score_cliente(db: Session, cliente_id: str) -> dict:
    """
    Obtener score total y desglose del cliente
    """
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        return None
    
    # Obtener actividades recientes (últimos 7 días)
    fecha_limite = datetime.utcnow() - timedelta(days=7)
    actividades_recientes = db.query(ActividadComercial).filter(
        ActividadComercial.cliente_id == cliente_id,
        ActividadComercial.created_at >= fecha_limite
    ).order_by(ActividadComercial.created_at.desc()).all()
    
    # Calcular puntos de la semana
    puntos_semana = sum(float(act.puntos_otorgados) for act in actividades_recientes)
    
    # Calcular puntos del día
    hoy = datetime.utcnow().date()
    puntos_hoy = sum(
        float(act.puntos_otorgados) 
        for act in actividades_recientes 
        if act.created_at.date() == hoy
    )
    
    return {
        'total_puntos': cliente.score_comercial,
        'puntos_dia': puntos_hoy,
        'puntos_semana': puntos_semana,
        'objetivo_diario': settings.SCORING_OBJETIVO_DIARIO,
        'objetivo_semanal': settings.SCORING_OBJETIVO_SEMANAL,
        'porcentaje_diario': round((puntos_hoy / settings.SCORING_OBJETIVO_DIARIO) * 100, 2),
        'porcentaje_semanal': round((puntos_semana / settings.SCORING_OBJETIVO_SEMANAL) * 100, 2),
        'actividades_recientes': actividades_recientes[:10]  # Últimas 10
    }


def obtener_actividades_cliente(
    db: Session, 
    cliente_id: str, 
    limit: int = 50
) -> list:
    """
    Obtener historial de actividades del cliente
    """
    actividades = db.query(ActividadComercial).filter(
        ActividadComercial.cliente_id == cliente_id
    ).order_by(
        ActividadComercial.created_at.desc()
    ).limit(limit).all()
    
    return actividades


def obtener_estadisticas_scoring(db: Session) -> dict:
    """
    Obtener estadísticas generales de scoring
    """
    # Total de puntos por todos los clientes
    total_puntos = db.query(func.sum(Cliente.score_comercial)).scalar() or 0
    
    # Promedio de puntos
    promedio_puntos = db.query(func.avg(Cliente.score_comercial)).scalar() or 0
    
    # Cliente con más puntos
    top_cliente = db.query(Cliente).order_by(
        Cliente.score_comercial.desc()
    ).first()
    
    # Actividades del día
    hoy = datetime.utcnow().date()
    actividades_hoy = db.query(ActividadComercial).filter(
        func.date(ActividadComercial.created_at) == hoy
    ).count()
    
    return {
        'total_puntos': total_puntos,
        'promedio_puntos': round(float(promedio_puntos), 2),
        'top_cliente': top_cliente.nombre_completo if top_cliente else None,
        'top_cliente_puntos': top_cliente.score_comercial if top_cliente else 0,
        'actividades_hoy': actividades_hoy
    }
