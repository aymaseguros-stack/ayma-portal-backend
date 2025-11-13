"""
Schemas de Dashboard y Scoring
"""
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class DashboardResumen(BaseModel):
    """Schema para dashboard del cliente"""
    cliente: dict
    cantidad_polizas: int
    polizas_vigentes: int
    cantidad_vehiculos: int
    proximas_renovaciones: List[dict]
    score_comercial: int
    ultima_actividad: Optional[datetime] = None


class ActividadComercialCreate(BaseModel):
    """Schema para crear actividad comercial"""
    cliente_id: str
    tipo_actividad: str
    puntos_otorgados: Decimal
    descripcion: Optional[str] = None
    metadata_json: Optional[str] = None


class ActividadComercialResponse(BaseModel):
    """Schema para respuesta de actividad"""
    id: str
    cliente_id: str
    tipo_actividad: str
    puntos_otorgados: Decimal
    descripcion: Optional[str] = None
    fecha_actividad: datetime
    
    class Config:
        from_attributes = True


class ScoringResumen(BaseModel):
    """Schema para resumen de scoring"""
    total_puntos: Decimal
    objetivo_diario: int
    objetivo_semanal: int
    porcentaje_diario: float
    porcentaje_semanal: float
    actividades_recientes: List[ActividadComercialResponse]


class EstadisticasPortal(BaseModel):
    """Schema para estadísticas del portal"""
    total_clientes: int
    clientes_activos: int
    total_polizas: int
    polizas_vigentes: int
    total_vehiculos: int
    score_promedio: float
