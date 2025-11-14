"""
API v1 package
"""
from fastapi import APIRouter
from .auth import router as auth_router
from .polizas import router as polizas_router
from .vehiculos import router as vehiculos_router
from .dashboard import router as dashboard_router
from .seed import router as seed_router

# Router principal para v1
api_router = APIRouter(prefix="/v1")

# Incluir todos los routers CON sus prefixes
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(polizas_router, prefix="/polizas", tags=["polizas"])
api_router.include_router(vehiculos_router, prefix="/vehiculos", tags=["vehiculos"])
api_router.include_router(seed_router, prefix="/seed", tags=["seed"])

__all__ = ["api_router"]
