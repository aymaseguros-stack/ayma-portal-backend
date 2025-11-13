"""
Modelo de Usuario
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"
    
    # ID como UUID (compatible con PostgreSQL y SQLite)
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Autenticación
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    tipo_usuario = Column(String(20), nullable=False)  # 'cliente', 'agente', 'admin'
    
    # Estado
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_ultimo_acceso = Column(DateTime, nullable=True)
    
    # Seguridad
    intentos_fallidos = Column(Integer, default=0)
    bloqueado_hasta = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    cliente = relationship(
        "Cliente", 
        back_populates="usuario", 
        foreign_keys="[Cliente.usuario_id]",
        uselist=False
    )
    
    def __repr__(self):
        return f"<Usuario {self.email} ({self.tipo_usuario})>"
