"""
Schemas de Póliza
"""
from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime
from decimal import Decimal


class PolizaBase(BaseModel):
    """Base para póliza"""
    numero_poliza: str
    compania: str  # 'San Cristóbal', 'Nación Seguros', 'Mapfre', 'SMG'
    ramo: str  # 'automotor', 'hogar', 'vida'
    tipo_cobertura: str  # 'RC', 'terceros_completo', 'todo_riesgo'
    fecha_inicio: date
    fecha_vencimiento: date
    premio_total: Decimal
    premio_mensual: Optional[Decimal] = None
    forma_pago: Optional[str] = None


class PolizaCreate(PolizaBase):
    """Schema para crear póliza"""
    cliente_id: str
    vehiculo_id: Optional[str] = None
    suma_asegurada: Optional[Decimal] = None
    tiene_franquicia: bool = False
    monto_franquicia: Optional[Decimal] = None
    cobertura_granizo: bool = False
    cobertura_cristales: bool = False
    cobertura_gnc: bool = False


class PolizaUpdate(BaseModel):
    """Schema para actualizar póliza"""
    fecha_vencimiento: Optional[date] = None
    premio_total: Optional[Decimal] = None
    premio_mensual: Optional[Decimal] = None
    estado: Optional[str] = None
    url_poliza_pdf: Optional[str] = None
    observaciones: Optional[str] = None


class PolizaResponse(PolizaBase):
    """Schema para respuesta de póliza"""
    id: str
    cliente_id: str
    vehiculo_id: Optional[str] = None
    numero_certificado: Optional[str] = None
    suma_asegurada: Optional[Decimal] = None
    estado: str
    tiene_franquicia: bool
    monto_franquicia: Optional[Decimal] = None
    cobertura_granizo: bool
    cobertura_cristales: bool
    cobertura_gnc: bool
    url_poliza_pdf: Optional[str] = None
    renovacion_automatica: bool
    created_at: datetime
    esta_vigente: bool
    dias_para_vencimiento: Optional[int] = None
    
    class Config:
        from_attributes = True


class PolizaResumen(BaseModel):
    """Schema para resumen de póliza en dashboard"""
    id: str
    numero_poliza: str
    compania: str
    tipo_cobertura: str
    fecha_vencimiento: date
    premio_mensual: Optional[Decimal] = None
    estado: str
    dias_para_vencimiento: Optional[int] = None
    
    class Config:
        from_attributes = True
