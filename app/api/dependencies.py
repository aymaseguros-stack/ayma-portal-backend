"""
Dependencies para endpoints - Autenticación y autorización
"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_token
from app.models import Usuario, Cliente
from app.services import auth as auth_service

# Security scheme
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Obtener usuario actual desde el token JWT
    """
    token = credentials.credentials
    
    # Decodificar token
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    
    # Verificar tipo de token
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tipo de token inválido"
        )
    
    # Obtener usuario
    email = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    usuario = auth_service.get_user_by_email(db, email)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )
    
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    return usuario


def get_current_cliente(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Cliente:
    """
    Obtener cliente actual (solo para usuarios tipo 'cliente')
    """
    if usuario.tipo_usuario != "cliente":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso solo para clientes"
        )
    
    cliente = auth_service.get_cliente_by_usuario_id(db, usuario.id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de cliente no encontrado"
        )
    
    return cliente


def require_admin(
    usuario: Usuario = Depends(get_current_user)
) -> Usuario:
    """
    Requerir que el usuario sea admin
    """
    if usuario.tipo_usuario != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso solo para administradores"
        )
    return usuario
