"""
Endpoints de Autenticación
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.schemas.auth import LoginRequest, LoginResponse, UserResponse
from app.models.usuario import Usuario

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login de usuario
    """
    # Buscar usuario
    user = db.query(Usuario).filter(Usuario.email == credentials.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )
    
    # Verificar contraseña
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )
    
    # Verificar que esté activo
    if not user.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    # Crear token
    access_token = create_access_token(data={"sub": user.email})
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        email=user.email,
        tipo_usuario=user.tipo_usuario.value  # ← NUEVO: devolver rol
    )
