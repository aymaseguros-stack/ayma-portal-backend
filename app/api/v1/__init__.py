"""
API v1 package
"""
from fastapi import APIRouter
from .auth import router as auth_router
from .polizas import router as polizas_router
from .vehiculos import router as vehiculos_router
from .dashboard import router as dashboard_router

# Router principal para v1
api_router = APIRouter(prefix="/v1")

# Incluir todos los routers
api_router.include_router(auth_router)
api_router.include_router(polizas_router)
api_router.include_router(vehiculos_router)
api_router.include_router(dashboard_router)

__all__ = ["api_router"]
