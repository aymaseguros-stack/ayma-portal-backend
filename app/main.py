"""
Portal AYMA Advisors - FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import init_db
from app.core.init_users import create_default_users
from app.api.v1 import api_router

app = FastAPI(
    title="Portal AYMA Advisors API",
    description="API para gestión de seguros y clientes",
    version="1.0.0"
)

# CORS - CONFIGURACIÓN PERMISIVA PARA DESARROLLO
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción usar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Incluir router API
app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """Inicializar base de datos y usuarios al arrancar"""
    print("🚀 Iniciando Portal AYMA Advisors API...")
    init_db()
    create_default_users()
    print("✅ Usuarios inicializados")


@app.get("/")
def root():
    """Endpoint raíz"""
    return {
        "message": "Portal AYMA Advisors API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
