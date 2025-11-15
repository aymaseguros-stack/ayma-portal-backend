"""
Endpoints de Dashboard
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models import Cliente, Poliza, Vehiculo, ActividadComercial
from app.schemas.dashboard import DashboardResumen, ScoringResumen
from app.services import scoring as scoring_service
from app.api.dependencies import get_current_cliente

router = APIRouter()


@router.get("/", response_model=DashboardResumen)
def obtener_dashboard(
    cliente: Cliente = Depends(get_current_cliente),
    db: Session = Depends(get_db)
):
    """
    Obtener resumen completo del dashboard para el cliente
    """
    cliente_info = {
        "id": cliente.id,
        "nombre_completo": f"{cliente.nombre} {cliente.apellido or ''}".strip(),
        "documento": f"{cliente.tipo_documento} {cliente.numero_documento}",
        "email": cliente.email,
        "celular": cliente.telefono or "",
        "score_comercial": cliente.scoring_comercial or 0
    }
    
    total_polizas = db.query(Poliza).filter(
        Poliza.cliente_id == cliente.id
    ).count()
    
    polizas_vigentes = db.query(Poliza).filter(
        Poliza.cliente_id == cliente.id,
        Poliza.estado == "vigente"
    ).count()
    
    total_vehiculos = db.query(Vehiculo).filter(
        Vehiculo.cliente_id == cliente.id
    ).count()
    
    fecha_limite = datetime.now().date() + timedelta(days=60)
    proximas_renovaciones = db.query(Poliza).filter(
        Poliza.cliente_id == cliente.id,
        Poliza.estado == "vigente",
        Poliza.fecha_vencimiento <= fecha_limite
    ).order_by(Poliza.fecha_vencimiento).all()
    
    renovaciones_info = [
        {
            "id": p.id,
            "numero_poliza": p.numero_poliza,
            "compania": p.compania,
            "tipo_cobertura": p.tipo_cobertura,
            "fecha_vencimiento": p.fecha_vencimiento.isoformat(),
            "dias_para_vencimiento": (p.fecha_vencimiento - datetime.now().date()).days
        }
        for p in proximas_renovaciones
    ]
    
    ultima_actividad = db.query(ActividadComercial).filter(
        ActividadComercial.cliente_id == cliente.id
    ).order_by(ActividadComercial.created_at.desc()).first()
    
    return DashboardResumen(
        cliente=cliente_info,
        cantidad_polizas=total_polizas,
        polizas_vigentes=polizas_vigentes,
        cantidad_vehiculos=total_vehiculos,
        proximas_renovaciones=renovaciones_info,
        score_comercial=cliente.scoring_comercial or 0,
        ultima_actividad=ultima_actividad.created_at if ultima_actividad else None
    )


@router.get("/scoring", response_model=ScoringResumen)
def obtener_scoring(
    cliente: Cliente = Depends(get_current_cliente),
    db: Session = Depends(get_db)
):
    score_data = scoring_service.obtener_score_cliente(db, cliente.id)
    
    if not score_data:
        return ScoringResumen(
            total_puntos=0,
            objetivo_diario=130,
            objetivo_semanal=840,
            porcentaje_diario=0,
            porcentaje_semanal=0,
            actividades_recientes=[]
        )
    
    return ScoringResumen(
        total_puntos=score_data['total_puntos'],
        objetivo_diario=score_data['objetivo_diario'],
        objetivo_semanal=score_data['objetivo_semanal'],
        porcentaje_diario=score_data['porcentaje_diario'],
        porcentaje_semanal=score_data['porcentaje_semanal'],
        actividades_recientes=score_data['actividades_recientes']
    )


@router.get("/actividades")
def obtener_actividades_recientes(
    cliente: Cliente = Depends(get_current_cliente),
    db: Session = Depends(get_db),
    limit: int = 20
):
    actividades = scoring_service.obtener_actividades_cliente(
        db,
        cliente.id,
        limit=limit
    )
    
    return [
        {
            "id": act.id,
            "tipo_actividad": act.tipo_actividad,
            "puntos_otorgados": float(act.puntos_otorgados),
            "descripcion": act.descripcion,
            "fecha": act.fecha_actividad.isoformat()
        }
        for act in actividades
    ]
