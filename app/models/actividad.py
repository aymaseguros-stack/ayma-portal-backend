"""
Modelo de Actividad Comercial - Sistema de Scoring
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Numeric, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class ActividadComercial(Base):
    __tablename__ = "actividades_comerciales"
    
    # ID
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Relaciones
    cliente_id = Column(String(36), ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False)
    agente_id = Column(String(36), ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True)
    
    # Tipo de actividad
    tipo_actividad = Column(String(100), nullable=False)
    # Valores posibles:
    # - 'login'
    # - 'ver_poliza'
    # - 'descargar_pdf'
    # - 'solicitar_cotizacion'
    # - 'llamado_nuevo'
    # - 'llamado_seguimiento'
    # - 'cotizado'
    # - 'propuesta_entregada'
    # - 'cliente_cerrado'
    # - 'cliente_perdido'
    
    # Puntos otorgados
    puntos_otorgados = Column(Numeric(5, 1), nullable=False)
    
    # Detalles
    descripcion = Column(Text, nullable=True)
    metadata_json = Column(Text, nullable=True)  # JSON como string
    
    # Timestamps
    fecha_actividad = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    cliente = relationship("Cliente", back_populates="actividades")
    
    def __repr__(self):
        return f"<ActividadComercial {self.tipo_actividad} - {self.puntos_otorgados} pts>"
