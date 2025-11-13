"""
Schemas de Cliente
"""
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class ClienteBase(BaseModel):
    """Base para cliente"""
    tipo_persona: str  # 'fisica', 'juridica'
    nombre: str
    apellido: Optional[str] = None
    razon_social: Optional[str] = None
    tipo_documento: str  # 'DNI', 'CUIT'
    numero_documento: str
    cuit_cuil: Optional[str] = None
    telefono: Optional[str] = None
    celular: Optional[str] = None
    email_contacto: Optional[EmailStr] = None
    calle: Optional[str] = None
    numero: Optional[str] = None
    piso: Optional[str] = None
    departamento: Optional[str] = None
    codigo_postal: Optional[str] = None
    localidad: Optional[str] = None
    provincia: Optional[str] = None
    pais: str = "Argentina"


class ClienteCreate(ClienteBase):
    """Schema para crear cliente"""
    usuario_id: Optional[str] = None


class ClienteUpdate(BaseModel):
    """Schema para actualizar cliente"""
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    celular: Optional[str] = None
    email_contacto: Optional[EmailStr] = None
    calle: Optional[str] = None
    numero: Optional[str] = None
    piso: Optional[str] = None
    departamento: Optional[str] = None
    codigo_postal: Optional[str] = None
    localidad: Optional[str] = None
    provincia: Optional[str] = None


class ClienteResponse(ClienteBase):
    """Schema para respuesta de cliente"""
    id: str
    usuario_id: str
    segmento: Optional[str] = None
    score_comercial: int = 0
    cantidad_polizas: int = 0
    estado: str
    fecha_alta: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class ClienteResumen(BaseModel):
    """Schema para resumen de cliente en dashboard"""
    id: str
    nombre_completo: str
    tipo_documento: str
    numero_documento: str
    cantidad_polizas: int
    cantidad_vehiculos: int
    score_comercial: int
    estado: str
    
    class Config:
        from_attributes = True
