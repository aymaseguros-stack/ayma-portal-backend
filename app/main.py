"""
Aplicación principal FastAPI - Portal AYMA Advisors
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.api.v1 import api_router

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API del Portal de Clientes AYMA Advisors",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(api_router, prefix="/api")


@app.on_event("startup")
def on_startup():
    """
    Evento al iniciar la aplicación
    """
    # Inicializar base de datos (crear tablas si no existen)
    init_db()
    print(f"✅ Base de datos inicializada")
    print(f"✅ {settings.PROJECT_NAME} v{settings.VERSION} iniciado")
    print(f"✅ Ambiente: {settings.ENVIRONMENT}")
    print(f"✅ Base de datos: {settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else settings.DATABASE_URL}")


@app.get("/")
def root():
    """
    Endpoint raíz
    """
    return {
        "message": "Portal AYMA Advisors API",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
