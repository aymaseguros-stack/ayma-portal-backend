"""
Schemas de Autenticación
"""
from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    """Schema de respuesta del token"""
    access_token: str
    token_type: str = "bearer"
    email: str
    tipo_usuario: str


class TokenData(BaseModel):
    """Schema de datos del token"""
    email: Optional[str] = None


class LoginRequest(BaseModel):
    """Schema de request de login"""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Schema de respuesta de login"""
    access_token: str
    token_type: str = "bearer"
    email: str
    tipo_usuario: str  # ← NUEVO


class PasswordChangeRequest(BaseModel):
    """Schema para cambiar contraseña"""
    old_password: str
    new_password: str


class UserResponse(BaseModel):
    """Schema de respuesta de usuario"""
    email: str
    tipo_usuario: str
    activo: bool
    
    class Config:
        from_attributes = True
