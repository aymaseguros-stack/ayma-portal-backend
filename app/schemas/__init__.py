"""
Schemas package - Pydantic schemas para validación
"""
from .auth import (
    LoginRequest,
    LoginResponse,
    TokenRefreshRequest,
    TokenRefreshResponse,
    UsuarioCreate,
    UsuarioResponse,
    ChangePasswordRequest
)
from .cliente import (
    ClienteCreate,
    ClienteUpdate,
    ClienteResponse,
    ClienteResumen
)
from .vehiculo import (
    VehiculoCreate,
    VehiculoUpdate,
    VehiculoResponse,
    VehiculoResumen
)
from .poliza import (
    PolizaCreate,
    PolizaUpdate,
    PolizaResponse,
    PolizaResumen
)
from .dashboard import (
    DashboardResumen,
    ActividadComercialCreate,
    ActividadComercialResponse,
    ScoringResumen,
    EstadisticasPortal
)

__all__ = [
    # Auth
    "LoginRequest",
    "LoginResponse",
    "TokenRefreshRequest",
    "TokenRefreshResponse",
    "UsuarioCreate",
    "UsuarioResponse",
    "ChangePasswordRequest",
    # Cliente
    "ClienteCreate",
    "ClienteUpdate",
    "ClienteResponse",
    "ClienteResumen",
    # Vehículo
    "VehiculoCreate",
    "VehiculoUpdate",
    "VehiculoResponse",
    "VehiculoResumen",
    # Póliza
    "PolizaCreate",
    "PolizaUpdate",
    "PolizaResponse",
    "PolizaResumen",
    # Dashboard
    "DashboardResumen",
    "ActividadComercialCreate",
    "ActividadComercialResponse",
    "ScoringResumen",
    "EstadisticasPortal",
]
