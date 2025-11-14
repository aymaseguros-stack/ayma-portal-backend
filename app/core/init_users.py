"""
Inicialización de usuarios por defecto
"""
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.usuario import Usuario, TipoUsuario
from app.core.security import get_password_hash


def create_default_users():
    """Crea usuarios por defecto si no existen"""
    db = SessionLocal()
    
    try:
        # Usuario ADMIN
        admin_email = "aymaseguros@hotmail.com"
        admin = db.query(Usuario).filter(Usuario.email == admin_email).first()
        
        if not admin:
            admin = Usuario(
                email=admin_email,
                password_hash=get_password_hash("Admin123456789"),
                tipo_usuario=TipoUsuario.ADMIN,  # ← Usar ENUM
                activo=True
            )
            db.add(admin)
            print(f"✅ Usuario ADMIN creado: {admin_email}")
        else:
            admin.tipo_usuario = TipoUsuario.ADMIN  # ← Usar ENUM
            print(f"✅ Usuario ADMIN actualizado: {admin_email}")
        
        # Usuario EMPLEADO
        empleado_email = "empleado@aymaseguros.com"
        empleado = db.query(Usuario).filter(Usuario.email == empleado_email).first()
        
        if not empleado:
            empleado = Usuario(
                email=empleado_email,
                password_hash=get_password_hash("Empleado123"),
                tipo_usuario=TipoUsuario.EMPLEADO,  # ← Usar ENUM
                activo=True
            )
            db.add(empleado)
            print(f"✅ Usuario EMPLEADO creado: {empleado_email}")
        
        # Usuario CLIENTE
        cliente_email = "cliente@ejemplo.com"
        cliente = db.query(Usuario).filter(Usuario.email == cliente_email).first()
        
        if not cliente:
            cliente = Usuario(
                email=cliente_email,
                password_hash=get_password_hash("Cliente123"),
                tipo_usuario=TipoUsuario.CLIENTE,  # ← Usar ENUM
                activo=True
            )
            db.add(cliente)
            print(f"✅ Usuario CLIENTE creado: {cliente_email}")
        
        db.commit()
        
        print("\n" + "="*50)
        print("📋 USUARIOS DE PRUEBA:")
        print("="*50)
        print(f"🔑 ADMIN: aymaseguros@hotmail.com / Admin123456789")
        print(f"👔 EMPLEADO: empleado@aymaseguros.com / Empleado123")
        print(f"👤 CLIENTE: cliente@ejemplo.com / Cliente123")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"❌ Error creando usuarios: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_default_users()
