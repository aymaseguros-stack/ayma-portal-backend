"""
Modelo de Cliente
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    usuario_id = Column(String(36), ForeignKey("usuarios.id"), nullable=True, index=True)
    
    # Datos básicos
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100))
    email = Column(String(255), nullable=False, index=True)
    telefono = Column(String(20))
    
    # Documento
    tipo_documento = Column(String(20), default="DNI")
    numero_documento = Column(String(20), nullable=False, unique=True, index=True)
    
    # Domicilio
    domicilio_calle = Column(String(200))
    domicilio_numero = Column(String(10))
    domicilio_ciudad = Column(String(100))
    domicilio_provincia = Column(String(50))
    domicilio_codigo_postal = Column(String(10))
    
    # Scoring
    scoring_comercial = Column(Integer, default=0)
    
    # Estado
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones (SIN back_populates a Usuario)
    polizas = relationship("Poliza", back_populates="cliente", foreign_keys="[Poliza.cliente_id]")
    vehiculos = relationship("Vehiculo", back_populates="cliente", foreign_keys="[Vehiculo.cliente_id]")
    actividades = relationship("ActividadComercial", back_populates="cliente")
    
    def __repr__(self):
        return f"<Cliente {self.nombre} {self.apellido or ''}>"
