"""
Schemas de Vehículo
"""
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class VehiculoBase(BaseModel):
    """Base para vehículo"""
    dominio: str
    tipo_vehiculo: str  # 'auto', 'moto', 'camion'
    marca: str
    modelo: str
    anio: int
    version: Optional[str] = None
    tipo_combustible: Optional[str] = None
    uso: str  # 'particular', 'comercial'
    tiene_garaje: bool = False
    tipo_garaje: Optional[str] = None


class VehiculoCreate(VehiculoBase):
    """Schema para crear vehículo"""
    cliente_id: str


class VehiculoUpdate(BaseModel):
    """Schema para actualizar vehículo"""
    kilometraje: Optional[int] = None
    tiene_garaje: Optional[bool] = None
    tipo_garaje: Optional[str] = None
    codigo_postal_guarda: Optional[str] = None
    estado: Optional[str] = None


class VehiculoResponse(VehiculoBase):
    """Schema para respuesta de vehículo"""
    id: str
    cliente_id: str
    estado: str
    fecha_alta: datetime
    descripcion_completa: str
    
    class Config:
        from_attributes = True


class VehiculoResumen(BaseModel):
    """Schema para resumen de vehículo"""
    id: str
    dominio: str
    descripcion_completa: str
    anio: int
    estado: str
    tiene_poliza_vigente: bool = False
    
    class Config:
        from_attributes = True
