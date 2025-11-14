"""
Schemas del proyecto
"""
from app.schemas.auth import (
    Token,
    TokenData,
    LoginRequest,
    LoginResponse,
    PasswordChangeRequest,
    UserResponse
)
from app.schemas.dashboard import (
    DashboardResumen,
    ScoringResumen
)
from app.schemas.poliza import (
    PolizaResponse,
    PolizaResumen,
    PolizaCreate
)
from app.schemas.vehiculo import (
    VehiculoResponse,
    VehiculoResumen
)

__all__ = [
    # Auth
    "Token",
    "TokenData", 
    "LoginRequest",
    "LoginResponse",
    "PasswordChangeRequest",
    "UserResponse",
    # Dashboard
    "DashboardResumen",
    "ScoringResumen",
    # Poliza
    "PolizaResponse",
    "PolizaResumen",
    "PolizaCreate",
    # Vehiculo
    "VehiculoResponse",
    "VehiculoResumen"
]
