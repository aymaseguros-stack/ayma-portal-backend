"""
Modelo de Usuario
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLEnum
from app.core.database import Base
import enum


class TipoUsuario(str, enum.Enum):
    ADMIN = "admin"
    EMPLEADO = "empleado"
    CLIENTE = "cliente"


class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # NUEVO: Tipo de usuario
    tipo_usuario = Column(SQLEnum(TipoUsuario), nullable=False, default=TipoUsuario.CLIENTE)
    
    # Estado
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Usuario {self.email} ({self.tipo_usuario})>"
