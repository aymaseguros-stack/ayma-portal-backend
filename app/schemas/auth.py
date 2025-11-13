"""
Schemas de Autenticación
"""
from typing import Optional
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Schema para login"""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Schema para respuesta de login"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict


class TokenRefreshRequest(BaseModel):
    """Schema para refresh token"""
    refresh_token: str


class TokenRefreshResponse(BaseModel):
    """Schema para respuesta de refresh"""
    access_token: str
    token_type: str = "bearer"


class UsuarioBase(BaseModel):
    """Base para usuario"""
    email: EmailStr
    tipo_usuario: str  # 'cliente', 'agente', 'admin'


class UsuarioCreate(UsuarioBase):
    """Schema para crear usuario"""
    password: str


class UsuarioResponse(UsuarioBase):
    """Schema para respuesta de usuario"""
    id: str
    activo: bool
    fecha_creacion: Optional[str] = None
    
    class Config:
        from_attributes = True


class ChangePasswordRequest(BaseModel):
    """Schema para cambiar contraseña"""
    old_password: str
    new_password: str
