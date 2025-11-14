"""
Endpoints administrativos - SOLO TEMPORAL
"""
from fastapi import APIRouter, HTTPException
from app.core.database import Base, engine
from app.models import Usuario, Poliza, Vehiculo, ActividadComercial
from app.core.init_users import create_default_users

router = APIRouter(tags=["admin"])


@router.post("/reset-database")
def reset_database(secret: str):
    """
    TEMPORAL: Resetea la base de datos
    Secret: ayma2025reset
    """
    if secret != "ayma2025reset":
        raise HTTPException(status_code=403, detail="Secret incorrecto")
    
    try:
        # Borrar tablas
        Base.metadata.drop_all(bind=engine)
        
        # Recrear tablas
        Base.metadata.create_all(bind=engine)
        
        # Crear usuarios
        create_default_users()
        
        return {
            "status": "success",
            "message": "Base de datos reseteada correctamente"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
