import sys
sys.path.insert(0, '/opt/render/project/src')

from app.core.database import SessionLocal
from app.models.usuario import Usuario
from app.core.security import get_password_hash

db = SessionLocal()

# Verificar si existe
existing = db.query(Usuario).filter(Usuario.email == "aymaseguros@hotmail.com").first()

if existing:
    print("✅ Usuario ya existe")
else:
    # Crear usuario
    user = Usuario(
        email="aymaseguros@hotmail.com",
        hashed_password=get_password_hash("Admin123456789"),
        nombre="Administrador",
        apellido="AYMA",
        tipo_usuario="admin",
        is_active=True
    )
    db.add(user)
    db.commit()
    print("✅ Usuario admin creado exitosamente")

db.close()
