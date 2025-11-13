"""
Configuración de la base de datos
Soporta SQLite para desarrollo y PostgreSQL para producción
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Crear engine según el tipo de base de datos
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False}  # Necesario para SQLite
    )
else:
    # PostgreSQL
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


def get_db():
    """
    Dependency para obtener sesión de base de datos
    Se usa en los endpoints con Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializar base de datos
    Crea todas las tablas si no existen
    """
    Base.metadata.create_all(bind=engine)
