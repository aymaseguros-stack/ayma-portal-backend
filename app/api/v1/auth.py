"""
Endpoints de Autenticación
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    TokenRefreshRequest,
    TokenRefreshResponse,
    ChangePasswordRequest
)
from app.services import auth as auth_service
from app.services import scoring as scoring_service
from app.api.dependencies import get_current_user
from app.models import Usuario

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login de usuario
    """
    # Autenticar
    usuario = auth_service.authenticate_user(
        db, 
        credentials.email, 
        credentials.password
    )
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )
    
    # Crear tokens
    access_token = create_access_token({"sub": usuario.email})
    refresh_token = create_refresh_token({"sub": usuario.email})
    
    # Si es cliente, registrar actividad de login
    if usuario.tipo_usuario == "cliente":
        cliente = auth_service.get_cliente_by_usuario_id(db, usuario.id)
        if cliente:
            scoring_service.registrar_actividad(
                db,
                cliente_id=cliente.id,
                tipo_actividad="login",
                descripcion="Login en el portal"
            )
    
    # Preparar respuesta
    user_data = {
        "id": usuario.id,
        "email": usuario.email,
        "tipo_usuario": usuario.tipo_usuario,
        "activo": usuario.activo
    }
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user_data
    )


@router.post("/refresh", response_model=TokenRefreshResponse)
def refresh_token(
    request: TokenRefreshRequest,
    db: Session = Depends(get_db)
):
    """
    Refrescar access token usando refresh token
    """
    # Decodificar refresh token
    payload = decode_token(request.refresh_token)
    
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido"
        )
    
    email = payload.get("sub")
    usuario = auth_service.get_user_by_email(db, email)
    
    if not usuario or not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no válido"
        )
    
    # Crear nuevo access token
    new_access_token = create_access_token({"sub": usuario.email})
    
    return TokenRefreshResponse(access_token=new_access_token)


@router.post("/change-password")
def change_password(
    request: ChangePasswordRequest,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cambiar contraseña del usuario actual
    """
    success = auth_service.change_password(
        db,
        usuario,
        request.old_password,
        request.new_password
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña actual incorrecta"
        )
    
    return {"message": "Contraseña actualizada exitosamente"}


@router.get("/me")
def get_current_user_info(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtener información del usuario actual
    """
    user_info = {
        "id": usuario.id,
        "email": usuario.email,
        "tipo_usuario": usuario.tipo_usuario,
        "activo": usuario.activo,
        "fecha_creacion": usuario.fecha_creacion.isoformat() if usuario.fecha_creacion else None,
        "fecha_ultimo_acceso": usuario.fecha_ultimo_acceso.isoformat() if usuario.fecha_ultimo_acceso else None
    }
    
    # Si es cliente, agregar info del perfil
    if usuario.tipo_usuario == "cliente":
        cliente = auth_service.get_cliente_by_usuario_id(db, usuario.id)
        if cliente:
            user_info["cliente"] = {
                "id": cliente.id,
                "nombre_completo": cliente.nombre_completo,
                "documento": f"{cliente.tipo_documento} {cliente.numero_documento}",
                "email_contacto": cliente.email_contacto,
                "celular": cliente.celular,
                "score_comercial": cliente.score_comercial,
                "cantidad_polizas": cliente.cantidad_polizas
            }
    
    return user_info
