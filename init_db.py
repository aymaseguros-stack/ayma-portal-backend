"""
Script para cargar datos iniciales de prueba
Ejecutar: python init_db.py
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from datetime import date, datetime, timedelta
from app.core.database import SessionLocal, init_db
from app.core.security import get_password_hash
from app.models import Usuario, Cliente, Vehiculo, Poliza

def create_initial_data():
    """
    Crear datos iniciales de prueba
    """
    print("🔄 Inicializando base de datos...")
    
    # Inicializar tablas
    init_db()
    
    db = SessionLocal()
    
    try:
        # Verificar si ya existen datos
        existing_user = db.query(Usuario).first()
        if existing_user:
            print("⚠️  Ya existen datos en la base de datos")
            response = input("¿Deseas borrar y recrear? (s/n): ")
            if response.lower() != 's':
                print("❌ Cancelado")
                return
            # Borrar todos los datos
            db.query(Poliza).delete()
            db.query(Vehiculo).delete()
            db.query(Cliente).delete()
            db.query(Usuario).delete()
            db.commit()
            print("🗑️  Datos anteriores eliminados")
        
        # Crear usuario admin
        print("👤 Creando usuario admin...")
        admin = Usuario(
            email="admin@ayma.com.ar",
            password_hash=get_password_hash("admin123"),
            tipo_usuario="admin",
            activo=True
        )
        db.add(admin)
        db.commit()
        print(f"   ✅ Admin creado: admin@ayma.com.ar / admin123")
        
        # Crear usuario cliente de prueba
        print("👤 Creando usuario cliente de prueba...")
        cliente_user = Usuario(
            email="cliente@ayma.com.ar",
            password_hash=get_password_hash("cliente123"),
            tipo_usuario="cliente",
            activo=True
        )
        db.add(cliente_user)
        db.commit()
        db.refresh(cliente_user)
        print(f"   ✅ Cliente creado: cliente@ayma.com.ar / cliente123")
        
        # Crear perfil de cliente
        print("📋 Creando perfil de cliente...")
        cliente = Cliente(
            usuario_id=cliente_user.id,
            tipo_persona="fisica",
            nombre="Juan",
            apellido="Pérez",
            tipo_documento="DNI",
            numero_documento="30123456",
            cuit_cuil="20-30123456-7",
            celular="+54 9 341 5551234",
            email_contacto="cliente@ayma.com.ar",
            calle="San Martín",
            numero="1234",
            codigo_postal="2000",
            localidad="Rosario",
            provincia="Santa Fe",
            pais="Argentina",
            segmento="persona",
            origen="web",
            estado="activo"
        )
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        print(f"   ✅ Perfil de cliente creado")
        
        # Crear vehículo
        print("🚗 Creando vehículo...")
        vehiculo = Vehiculo(
            cliente_id=cliente.id,
            dominio="AB123CD",
            tipo_vehiculo="auto",
            marca="Ford",
            modelo="Focus",
            anio=2020,
            version="SE Plus 2.0",
            tipo_combustible="nafta",
            uso="particular",
            tiene_garaje=True,
            tipo_garaje="privado",
            estado="activo"
        )
        db.add(vehiculo)
        db.commit()
        db.refresh(vehiculo)
        print(f"   ✅ Vehículo creado: {vehiculo.dominio}")
        
        # Crear póliza
        print("📄 Creando póliza...")
        fecha_inicio = date.today() - timedelta(days=90)
        fecha_vencimiento = fecha_inicio + timedelta(days=365)
        
        poliza = Poliza(
            cliente_id=cliente.id,
            vehiculo_id=vehiculo.id,
            numero_poliza="SC-2024-001234",
            numero_certificado="CERT-001234",
            compania="San Cristóbal",
            ramo="automotor",
            tipo_cobertura="Terceros Completo",
            fecha_inicio=fecha_inicio,
            fecha_vencimiento=fecha_vencimiento,
            estado="vigente",
            suma_asegurada=3500000.00,
            premio_total=48000.00,
            premio_mensual=4000.00,
            forma_pago="mensual",
            tiene_franquicia=False,
            cobertura_granizo=True,
            cobertura_cristales=True,
            cobertura_gnc=False,
            renovacion_automatica=True,
            observaciones="Póliza de prueba para testing del portal"
        )
        db.add(poliza)
        
        # Actualizar contador de pólizas del cliente
        cliente.cantidad_polizas = 1
        
        db.commit()
        db.refresh(poliza)
        print(f"   ✅ Póliza creada: {poliza.numero_poliza}")
        
        print("\n" + "="*60)
        print("✅ DATOS INICIALES CREADOS EXITOSAMENTE")
        print("="*60)
        print("\n🔐 Credenciales de acceso:")
        print("\n   ADMIN:")
        print("   Email: admin@ayma.com.ar")
        print("   Password: admin123")
        print("\n   CLIENTE:")
        print("   Email: cliente@ayma.com.ar")
        print("   Password: cliente123")
        print("\n📊 Datos creados:")
        print(f"   - 1 usuario admin")
        print(f"   - 1 cliente (Juan Pérez)")
        print(f"   - 1 vehículo (Ford Focus 2020)")
        print(f"   - 1 póliza vigente (San Cristóbal)")
        print("\n🚀 Ahora puedes iniciar el servidor:")
        print("   uvicorn app.main:app --reload")
        print("\n📚 Y probar el login en: http://localhost:8000/docs")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_initial_data()
