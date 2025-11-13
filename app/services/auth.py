"""
Servicio de Autenticación
"""
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from app.models import Usuario, Cliente
from app.core.security import verify_password, get_password_hash
from app.schemas.auth import UsuarioCreate


def authenticate_user(db: Session, email: str, password: str) -> Optional[Usuario]:
    """
    Autenticar usuario con email y contraseña
    """
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    
    if not usuario:
        return None
    
    if not usuario.activo:
        return None
    
    # Verificar si está bloqueado
    if usuario.bloqueado_hasta and usuario.bloqueado_hasta > datetime.utcnow():
        return None
    
    # Verificar contraseña
    if not verify_password(password, usuario.password_hash):
        # Incrementar intentos fallidos
        usuario.intentos_fallidos += 1
        if usuario.intentos_fallidos >= 5:
            # Bloquear por 30 minutos
            from datetime import timedelta
            usuario.bloqueado_hasta = datetime.utcnow() + timedelta(minutes=30)
        db.commit()
        return None
    
    # Login exitoso - resetear intentos fallidos
    usuario.intentos_fallidos = 0
    usuario.bloqueado_hasta = None
    usuario.fecha_ultimo_acceso = datetime.utcnow()
    db.commit()
    
    return usuario


def create_user(db: Session, user_data: UsuarioCreate) -> Usuario:
    """
    Crear nuevo usuario
    """
    # Verificar si ya existe
    existing_user = db.query(Usuario).filter(Usuario.email == user_data.email).first()
    if existing_user:
        raise ValueError("Usuario con este email ya existe")
    
    # Crear usuario
    hashed_password = get_password_hash(user_data.password)
    
    usuario = Usuario(
        email=user_data.email,
        password_hash=hashed_password,
        tipo_usuario=user_data.tipo_usuario,
        activo=True
    )
    
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    
    return usuario


def get_user_by_email(db: Session, email: str) -> Optional[Usuario]:
    """
    Obtener usuario por email
    """
    return db.query(Usuario).filter(Usuario.email == email).first()


def get_user_by_id(db: Session, user_id: str) -> Optional[Usuario]:
    """
    Obtener usuario por ID
    """
    return db.query(Usuario).filter(Usuario.id == user_id).first()


def get_cliente_by_usuario_id(db: Session, usuario_id: str) -> Optional[Cliente]:
    """
    Obtener cliente asociado a un usuario
    """
    return db.query(Cliente).filter(Cliente.usuario_id == usuario_id).first()


def change_password(db: Session, usuario: Usuario, old_password: str, new_password: str) -> bool:
    """
    Cambiar contraseña de usuario
    """
    # Verificar contraseña actual
    if not verify_password(old_password, usuario.password_hash):
        return False
    
    # Actualizar contraseña
    usuario.password_hash = get_password_hash(new_password)
    db.commit()
    
    return True
