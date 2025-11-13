from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Imports de routers
from app.api.v1 import auth, dashboard, polizas, vehiculos
from app.core.database import init_db
from app.core.init_users import create_default_users

# Crear aplicación
app = FastAPI(
    title="Portal AYMA Advisors API",
    description="API para gestión de seguros y clientes",
    version="1.0.0"
)

# Configurar CORS
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://portal-ayma.vercel.app",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["dashboard"])
app.include_router(polizas.router, prefix="/api/v1/polizas", tags=["polizas"])
app.include_router(vehiculos.router, prefix="/api/v1/vehiculos", tags=["vehiculos"])

# Evento de startup
@app.on_event("startup")
def on_startup():
    """Inicializar base de datos y usuarios al iniciar"""
    print("🚀 Iniciando Portal AYMA Advisors API...")
    
    # Inicializar tablas
    init_db()
    print("✅ Base de datos inicializada")
    
    # Crear usuarios por defecto
    create_default_users()
    print("✅ Usuarios inicializados")

# Endpoint raíz
@app.get("/")
async def root():
    return {
        "message": "Portal AYMA Advisors API",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "docs": "/docs",
        "health": "/health"
    }

# Health check para Render
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "AYMA Portal API"
    }
