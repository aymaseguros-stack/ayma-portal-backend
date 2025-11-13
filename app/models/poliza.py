"""
Modelo de Póliza
"""
import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Date, Numeric, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Poliza(Base):
    __tablename__ = "polizas"
    
    # ID
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Relaciones
    cliente_id = Column(String(36), ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False)
    vehiculo_id = Column(String(36), ForeignKey("vehiculos.id", ondelete="SET NULL"), nullable=True)
    
    # Identificación
    numero_poliza = Column(String(50), unique=True, nullable=False, index=True)
    numero_certificado = Column(String(50), nullable=True)
    
    # Aseguradora
    compania = Column(String(100), nullable=False)  # 'San Cristóbal', 'Nación', etc
    productor_codigo = Column(String(50), nullable=True)
    organizador = Column(String(100), nullable=True)
    
    # Tipo de Cobertura
    ramo = Column(String(100), nullable=False)  # 'automotor', 'hogar', 'vida'
    tipo_cobertura = Column(String(100), nullable=False)  # 'RC', 'terceros_completo'
    
    # Vigencia
    fecha_inicio = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    estado = Column(String(20), default="vigente")  # 'vigente', 'vencida', 'cancelada'
    
    # Valores
    suma_asegurada = Column(Numeric(12, 2), nullable=True)
    premio_total = Column(Numeric(10, 2), nullable=False)
    premio_mensual = Column(Numeric(10, 2), nullable=True)
    forma_pago = Column(String(50), nullable=True)  # 'mensual', 'anual'
    
    # Franquicia
    tiene_franquicia = Column(Boolean, default=False)
    tipo_franquicia = Column(String(50), nullable=True)
    monto_franquicia = Column(Numeric(10, 2), nullable=True)
    
    # Coberturas Adicionales
    cobertura_granizo = Column(Boolean, default=False)
    cobertura_cristales = Column(Boolean, default=False)
    cobertura_cerraduras = Column(Boolean, default=False)
    cobertura_gnc = Column(Boolean, default=False)
    
    # Documentación
    url_poliza_pdf = Column(String(500), nullable=True)
    url_certificado_pdf = Column(String(500), nullable=True)
    
    # Renovación
    fecha_renovacion = Column(Date, nullable=True)
    renovacion_automatica = Column(Boolean, default=True)
    
    # Metadata
    observaciones = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    cliente = relationship("Cliente", back_populates="polizas")
    vehiculo = relationship("Vehiculo", back_populates="polizas")
    
    def __repr__(self):
        return f"<Poliza {self.numero_poliza} - {self.compania} ({self.estado})>"
    
    @property
    def esta_vigente(self):
        return self.estado == "vigente" and self.fecha_vencimiento >= date.today()
    
    @property
    def dias_para_vencimiento(self):
        if self.fecha_vencimiento:
            delta = self.fecha_vencimiento - date.today()
            return delta.days
        return None
