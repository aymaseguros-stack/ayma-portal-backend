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
                password_hash=get_password_hash("Admin123456789"),
                tipo_usuario="admin",
                activo=True
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print(f"✅ Usuario administrador creado: {admin_user.email}")
        else:
            print(f"✅ Usuario administrador ya existe: {existing_admin.email}")
            
    except IntegrityError as e:
        print(f"⚠️ Error de integridad: {e}")
        db.rollback()
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()
