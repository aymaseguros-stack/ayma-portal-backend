"""
Endpoint temporal para poblar datos de prueba
"""
from fastapi import APIRouter, HTTPException
from app.core.database import SessionLocal
from app.models.usuario import Usuario
from app.models.cliente import Cliente
from app.models.poliza import Poliza
from app.models.vehiculo import Vehiculo
from app.models.actividad import ActividadComercial
from datetime import datetime, timedelta

router = APIRouter(tags=["seed"])


@router.post("/seed-data")
def seed_data(secret: str):
    """
    TEMPORAL: Poblar base de datos con datos de prueba
    Secret: ayma2025seed
    """
    if secret != "ayma2025seed":
        raise HTTPException(status_code=403, detail="Secret incorrecto")
    
    db = SessionLocal()
    
    try:
        # Buscar usuario cliente
        cliente_usuario = db.query(Usuario).filter(
            Usuario.email == "cliente@ejemplo.com"
        ).first()
        
        if not cliente_usuario:
            raise HTTPException(status_code=404, detail="Usuario cliente no encontrado")
        
        # Crear perfil de cliente
        cliente_existente = db.query(Cliente).filter(
            Cliente.usuario_id == cliente_usuario.id
        ).first()
        
        if not cliente_existente:
            cliente = Cliente(
                usuario_id=cliente_usuario.id,
                nombre="Juan",
                apellido="Pérez",
                email="cliente@ejemplo.com",
                telefono="341-1234567",
                tipo_documento="DNI",
                numero_documento="12345678",
                domicilio_calle="San Martín",
                domicilio_numero="123",
                domicilio_ciudad="Rosario",
                domicilio_provincia="Santa Fe",
                domicilio_codigo_postal="2000",
                scoring_comercial=0
            )
            db.add(cliente)
            db.flush()
        else:
            cliente = cliente_existente
        
        # Crear vehículos
        vehiculos = []
        if not db.query(Vehiculo).filter(Vehiculo.patente == "ABC123").first():
            veh1 = Vehiculo(
                cliente_id=cliente.id,
                patente="ABC123",
                marca="Toyota",
                modelo="Corolla",
                anio=2020,
                tipo="sedan",
                motor="1.8",
                chasis="JTDBT123400012345"
            )
            db.add(veh1)
            vehiculos.append(veh1)
        
        if not db.query(Vehiculo).filter(Vehiculo.patente == "XYZ789").first():
            veh2 = Vehiculo(
                cliente_id=cliente.id,
                patente="XYZ789",
                marca="Ford",
                modelo="Focus",
                anio=2019,
                tipo="sedan",
                motor="2.0",
                chasis="1FADP3K20HL123456"
            )
            db.add(veh2)
            vehiculos.append(veh2)
        
        db.flush()
        
        # Crear pólizas
        if not db.query(Poliza).filter(Poliza.numero_poliza == "POL-2024-001").first():
            pol1 = Poliza(
                cliente_id=cliente.id,
                vehiculo_id=vehiculos[0].id if vehiculos else None,
                numero_poliza="POL-2024-001",
                tipo_seguro="Auto",
                compania="San Cristóbal",
                vigencia_desde=datetime.now(),
                vigencia_hasta=datetime.now() + timedelta(days=365),
                premio=25000.0,
                cobertura="Terceros Completo",
                estado="vigente"
            )
            db.add(pol1)
        
        if not db.query(Poliza).filter(Poliza.numero_poliza == "POL-2024-002").first():
            pol2 = Poliza(
                cliente_id=cliente.id,
                vehiculo_id=vehiculos[1].id if len(vehiculos) > 1 else None,
                numero_poliza="POL-2024-002",
                tipo_seguro="Auto",
                compania="Mapfre",
                vigencia_desde=datetime.now(),
                vigencia_hasta=datetime.now() + timedelta(days=365),
                premio=30000.0,
                cobertura="Todo Riesgo",
                estado="vigente"
            )
            db.add(pol2)
        
        if not db.query(Poliza).filter(Poliza.numero_poliza == "POL-2024-003").first():
            pol3 = Poliza(
                cliente_id=cliente.id,
                numero_poliza="POL-2024-003",
                tipo_seguro="Hogar",
                compania="Nación Seguros",
                vigencia_desde=datetime.now(),
                vigencia_hasta=datetime.now() + timedelta(days=365),
                premio=15000.0,
                cobertura="Incendio y Robo",
                estado="vigente"
            )
            db.add(pol3)
        
        # Crear actividades
        act1 = ActividadComercial(
            cliente_id=cliente.id,
            usuario_id=cliente_usuario.id,
            tipo="llamado_nuevo",
            puntos=5.9,
            descripcion="Primer contacto con cliente",
            fecha=datetime.now() - timedelta(days=10)
        )
        db.add(act1)
        
        act2 = ActividadComercial(
            cliente_id=cliente.id,
            usuario_id=cliente_usuario.id,
            tipo="cotizado",
            puntos=13,
            descripcion="Cotización de seguro auto",
            fecha=datetime.now() - timedelta(days=5)
        )
        db.add(act2)
        
        db.commit()
        
        return {
            "status": "success",
            "message": "Datos de prueba creados correctamente",
            "data": {
                "cliente": f"{cliente.nombre} {cliente.apellido}",
                "vehiculos": 2,
                "polizas": 3,
                "actividades": 2
            }
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
