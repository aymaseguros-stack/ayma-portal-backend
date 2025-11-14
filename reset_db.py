"""
Script para resetear la base de datos
"""
from app.core.database import Base, engine
from app.models import Usuario, Poliza, Vehiculo, ActividadComercial
from app.core.init_users import create_default_users

print("🗑️  Borrando tablas...")
Base.metadata.drop_all(bind=engine)
print("✅ Tablas borradas")

print("🔧 Recreando tablas...")
Base.metadata.create_all(bind=engine)
print("✅ Tablas recreadas")

print("\n👥 Creando usuarios...")
create_default_users()
print("\n✅ Base de datos reseteada correctamente")
