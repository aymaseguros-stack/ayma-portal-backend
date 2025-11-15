"""
Dependencias compartidas para endpoints
"""
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.usuario import Usuario
from app.models.cliente import Cliente
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Obtener usuario actual desde el token JWT
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    
    email = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )
    
    return usuario


def get_current_cliente(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Cliente:
    """
    Obtener el perfil de Cliente asociado al usuario actual
    """
    # Buscar el Cliente asociado al usuario
    cliente = db.query(Cliente).filter(Cliente.usuario_id == usuario.id).first()
    
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró perfil de cliente para este usuario"
        )
    
    return cliente
