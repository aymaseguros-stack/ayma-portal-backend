"""
Configuración de la aplicación AYMA Portal
"""
import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Proyecto
    PROJECT_NAME: str = "AYMA Advisors - Portal de Clientes"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Base de datos
    # Para desarrollo usa SQLite, para producción PostgreSQL
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./ayma_portal.db"  # SQLite para desarrollo local
    )
    
    # Seguridad
    SECRET_KEY: str = os.getenv("SECRET_KEY", "ayma-secret-key-change-in-production-2025")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "https://portal-ayma.vercel.app",
    ]
    
    # Frontend URL
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # Redis (opcional para desarrollo)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Storage (para PDFs)
    STORAGE_TYPE: str = os.getenv("STORAGE_TYPE", "local")  # local, s3
    STORAGE_PATH: str = os.getenv("STORAGE_PATH", "./storage")
    
    # Email (para futuro)
    SMTP_HOST: str = os.getenv("SMTP_HOST", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    
    # WhatsApp (para futuro)
    WHATSAPP_API_KEY: str = os.getenv("WHATSAPP_API_KEY", "")
    
    # Sistema de scoring
    SCORING_OBJETIVO_DIARIO: int = 130
    SCORING_OBJETIVO_SEMANAL: int = 840
    
    # Puntos por acción del cliente
    PUNTOS_LOGIN: int = 1
    PUNTOS_VER_POLIZA: int = 2
    PUNTOS_DESCARGAR_PDF: int = 3
    PUNTOS_SOLICITAR_COTIZACION: int = 13
    
    # Puntos por acción comercial
    PUNTOS_LLAMADO_NUEVO: float = 5.9
    PUNTOS_LLAMADO_SEGUIMIENTO: int = 2
    PUNTOS_COTIZADO: int = 13
    PUNTOS_PROPUESTA_ENTREGADA: int = 25
    PUNTOS_CLIENTE_CERRADO: int = 50
    PUNTOS_CLIENTE_PERDIDO: int = -50
    
    class Config:
        case_sensitive = True


settings = Settings()
