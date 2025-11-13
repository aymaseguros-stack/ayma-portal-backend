"""
Inicialización de usuarios por defecto
"""
from app.core.database import SessionLocal
from app.models.usuario import Usuario
from app.core.security import get_password_hash
from sqlalchemy.exc import IntegrityError

def create_default_users():
    """
    Crea usuarios por defecto si no existen
    """
    db = SessionLocal()
    
    try:
        # Verificar si existe el usuario admin
        existing_admin = db.query(Usuario).filter(
            Usuario.email == "aymaseguros@hotmail.com"
        ).first()
        
        if not existing_admin:
            print("📝 Creando usuario administrador...")
            admin_user = Usuario(
                email="aymaseguros@hotmail.com",
                hashed_password=get_password_hash("Admin123456789"),
                nombre="Administrador",
                apellido="AYMA",
                tipo_usuario="admin",
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("✅ Usuario administrador creado exitosamente")
        else:
            print("✅ Usuario administrador ya existe")
            
    except IntegrityError as e:
        print(f"⚠️ Error al crear usuario: {e}")
        db.rollback()
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        db.rollback()
    finally:
        db.close()
