from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.core.database import init_db
from app.core.init_users import create_default_users
from app.api.v1 import api_router  # ← Solo importar el router agrupado

app = FastAPI(
    title="Portal AYMA Advisors API",
    description="API para gestión de seguros y clientes",
    version="1.0.0"
)

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://portal-ayma.vercel.app",
    "https://ayma-portal-frontend.vercel.app",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ SOLO ESTA LÍNEA - incluir el router agrupado
app.include_router(api_router, prefix="/api")

@app.on_event("startup")
def on_startup():
    """Inicializar base de datos y usuarios al iniciar"""
    print("🚀 Iniciando Portal AYMA Advisors API...")
    
    init_db()
    print("✅ Base de datos inicializada")
    
    create_default_users()
    print("✅ Usuarios inicializados")

@app.get("/")
async def root():
    return {
        "message": "Portal AYMA Advisors API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AYMA Portal API"}
