"""
Modelo de Vehículo
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Vehiculo(Base):
    __tablename__ = "vehiculos"
    
    # ID
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    cliente_id = Column(String(36), ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False)
    
    # Identificación
    dominio = Column(String(10), unique=True, nullable=False, index=True)
    tipo_vehiculo = Column(String(50), nullable=False)  # 'auto', 'moto', 'camion'
    
    # Datos del Vehículo
    marca = Column(String(100), nullable=False)
    modelo = Column(String(100), nullable=False)
    anio = Column(Integer, nullable=False)
    version = Column(String(255), nullable=True)
    
    # Especificaciones Técnicas
    tipo_combustible = Column(String(20), nullable=True)  # 'nafta', 'diesel', 'gnc'
    cilindrada = Column(String(20), nullable=True)
    potencia = Column(String(20), nullable=True)
    
    # Identificadores
    numero_motor = Column(String(50), nullable=True)
    numero_chasis = Column(String(50), nullable=True)
    
    # Uso
    uso = Column(String(50), nullable=False)  # 'particular', 'comercial'
    kilometraje = Column(Integer, nullable=True)
    
    # Garaje
    tiene_garaje = Column(Boolean, default=False)
    tipo_garaje = Column(String(50), nullable=True)  # 'privado', 'publico'
    codigo_postal_guarda = Column(String(10), nullable=True)
    
    # Estado
    estado = Column(String(20), default="activo")  # 'activo', 'vendido'
    fecha_alta = Column(DateTime, default=datetime.utcnow)
    fecha_baja = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    cliente = relationship("Cliente", back_populates="vehiculos")
    polizas = relationship("Poliza", back_populates="vehiculo")
    
    def __repr__(self):
        return f"<Vehiculo {self.dominio} - {self.marca} {self.modelo} ({self.anio})>"
    
    @property
    def descripcion_completa(self):
        return f"{self.marca} {self.modelo} {self.version or ''} {self.anio}".strip()
