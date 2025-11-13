"""
Modelo de Cliente
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Numeric, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Cliente(Base):
    __tablename__ = "clientes"
    
    # ID
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    usuario_id = Column(String(36), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    
    # Datos Personales
    tipo_persona = Column(String(20), nullable=False)  # 'fisica', 'juridica'
    nombre = Column(String(255), nullable=False)
    apellido = Column(String(255), nullable=True)
    razon_social = Column(String(255), nullable=True)
    
    # Documentos
    tipo_documento = Column(String(10), nullable=False)  # 'DNI', 'CUIT', etc
    numero_documento = Column(String(20), unique=True, nullable=False, index=True)
    cuit_cuil = Column(String(13), nullable=True)
    
    # Contacto
    telefono = Column(String(20), nullable=True)
    celular = Column(String(20), nullable=True)
    email_contacto = Column(String(255), nullable=True)
    
    # Dirección
    calle = Column(String(255), nullable=True)
    numero = Column(String(10), nullable=True)
    piso = Column(String(10), nullable=True)
    departamento = Column(String(10), nullable=True)
    codigo_postal = Column(String(10), nullable=True)
    localidad = Column(String(100), nullable=True)
    provincia = Column(String(100), nullable=True)
    pais = Column(String(100), default="Argentina")
    
    # Segmentación Comercial
    segmento = Column(String(50), nullable=True)  # 'persona', 'pyme', 'empresa'
    origen = Column(String(50), nullable=True)  # 'web', 'referido', etc
    agente_asignado = Column(String(36), ForeignKey("usuarios.id"), nullable=True)
    
    # Scoring y Métricas
    score_comercial = Column(Integer, default=0)
    valor_cartera = Column(Numeric(12, 2), default=0)
    cantidad_polizas = Column(Integer, default=0)
    antiguedad_meses = Column(Integer, default=0)
    
    # Estado
    estado = Column(String(20), default="activo")  # 'activo', 'inactivo', 'moroso'
    fecha_alta = Column(DateTime, default=datetime.utcnow)
    fecha_baja = Column(DateTime, nullable=True)
    motivo_baja = Column(Text, nullable=True)
    
    # Metadata
    notas = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="cliente", foreign_keys=[usuario_id])
    vehiculos = relationship("Vehiculo", back_populates="cliente", cascade="all, delete-orphan")
    polizas = relationship("Poliza", back_populates="cliente", cascade="all, delete-orphan")
    actividades = relationship("ActividadComercial", back_populates="cliente", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Cliente {self.nombre} {self.apellido or ''} - {self.numero_documento}>"
    
    @property
    def nombre_completo(self):
        if self.tipo_persona == "fisica":
            return f"{self.nombre} {self.apellido or ''}".strip()
        else:
            return self.razon_social or self.nombre
