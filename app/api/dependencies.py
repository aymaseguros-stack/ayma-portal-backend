"""
Dependencies y middleware de autenticación
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.core.database import get_db
from app.models.usuario import Usuario, TipoUsuario
from app.core.config import settings

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    """Obtiene el usuario actual desde el token JWT"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        
        if email is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    user = db.query(Usuario).filter(Usuario.email == email).first()
    
    if user is None or not user.activo:
        raise credentials_exception
    
    return user


def get_current_cliente(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Dependency para obtener cliente actual
    Por ahora solo retorna el usuario (sin modelo Cliente separado)
    """
    # TODO: Cuando tengamos modelo Cliente, buscarlo aquí
    return current_user


def require_admin(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """Requiere que el usuario sea administrador"""
    if current_user.tipo_usuario != TipoUsuario.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos de administrador"
        )
    return current_user


def require_empleado(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """Requiere que el usuario sea empleado o admin"""
    if current_user.tipo_usuario not in [TipoUsuario.ADMIN, TipoUsuario.EMPLEADO]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requiere permisos de empleado"
        )
    return current_user
