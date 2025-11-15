"""
Endpoint para cargar datos REALES en producción
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from decimal import Decimal
import uuid

from app.core.database import get_db
from app.core.security import get_password_hash
from app.models import Usuario, Cliente, Poliza, Vehiculo, ActividadComercial

router = APIRouter()


@router.post("/cargar-datos-reales")
def cargar_datos_reales(
    secret: str,
    db: Session = Depends(get_db)
):
    """Cargar datos reales de clientes (PRODUCCIÓN)"""
    
    if secret != "ayma2025real":
        raise HTTPException(status_code=403, detail="Secret incorrecto")
    
    # Limpiar datos de prueba
    db.query(ActividadComercial).delete()
    db.query(Poliza).delete()
    db.query(Vehiculo).delete()
    db.query(Cliente).delete()
    db.query(Usuario).filter(Usuario.email != "aymaseguros@hotmail.com").delete()
    db.commit()
    
    # Crear usuario principal
    usuario = Usuario(
        id=str(uuid.uuid4()),
        email="aybatista@icloud.com",
        password_hash=get_password_hash("Batista2025!"),
        tipo_usuario="cliente",
        activo=True
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    
    # Crear clientes
    c1 = Cliente(id=str(uuid.uuid4()), usuario_id=usuario.id, nombre="VICTOR ADRIAN", apellido="BATISTA", email="aybatista@icloud.com", telefono="+5493415923683", tipo_documento="CUIT", numero_documento="27235014241", domicilio_calle="B HOUSSEY", domicilio_numero="2875", domicilio_ciudad="ROLDAN", domicilio_provincia="SANTA FE", domicilio_codigo_postal="2134", scoring_comercial=0)
    c2 = Cliente(id=str(uuid.uuid4()), usuario_id=usuario.id, nombre="MATIAS", apellido="GONZALEZ", email="aybatista@icloud.com", telefono="+5493415923683", tipo_documento="CUIT", numero_documento="20396629292", domicilio_calle="BERNARDO HOUSSEY", domicilio_numero="2875", domicilio_ciudad="ROLDAN", domicilio_provincia="SANTA FE", domicilio_codigo_postal="2134", scoring_comercial=0)
    c3 = Cliente(id=str(uuid.uuid4()), usuario_id=usuario.id, nombre="VICTOR FACUNDO", apellido="BATISTA", email="aybatista@icloud.com", telefono="+5493415923683", tipo_documento="CUIT", numero_documento="20370734276", domicilio_calle="BERNARDO HOUSSAY", domicilio_numero="2875", domicilio_ciudad="ROLDAN", domicilio_provincia="SANTA FE", domicilio_codigo_postal="2134", scoring_comercial=0)
    
    db.add_all([c1, c2, c3])
    db.commit()
    for c in [c1, c2, c3]:
        db.refresh(c)
    
    # Vehículos y pólizas
    v1 = Vehiculo(id=str(uuid.uuid4()), cliente_id=c1.id, dominio="AOC153", tipo_vehiculo="AUTO", marca="FORD", modelo="FIESTA 1.6 5P SE PLUS", anio=2014, numero_motor="HXJCE729381", numero_chasis="9BFZD55N1EB729381", uso="PARTICULAR")
    db.add(v1)
    db.flush()
    db.add(Poliza(id=str(uuid.uuid4()), cliente_id=c1.id, vehiculo_id=v1.id, numero_poliza="2514460-V1", compania="NACION SEGUROS", ramo="AUTOMOTORES", tipo_cobertura="C80", fecha_inicio=datetime(2025, 10, 27).date(), fecha_vencimiento=datetime(2026, 10, 27).date(), suma_asegurada=Decimal("15708000"), premio_total=Decimal("43890.75"), estado="vigente"))
    
    v2 = Vehiculo(id=str(uuid.uuid4()), cliente_id=c1.id, dominio="NCX816", tipo_vehiculo="AUTO", marca="HONDA", modelo="CIVIC 1.8 EXS", anio=2013, numero_motor="R18Z14602407", numero_chasis="93HFB2680EZ602421", uso="PARTICULAR")
    db.add(v2)
    db.flush()
    db.add(Poliza(id=str(uuid.uuid4()), cliente_id=c1.id, vehiculo_id=v2.id, numero_poliza="2514460-V2", compania="NACION SEGUROS", ramo="AUTOMOTORES", tipo_cobertura="CN C", fecha_inicio=datetime(2025, 10, 27).date(), fecha_vencimiento=datetime(2026, 10, 27).date(), suma_asegurada=Decimal("17380000"), premio_total=Decimal("52264.67"), estado="vigente"))
    
    v3 = Vehiculo(id=str(uuid.uuid4()), cliente_id=c1.id, dominio="AD829NC", tipo_vehiculo="AUTO", marca="CITROEN", modelo="C3 1.6 VTI FEEL", anio=2019, numero_motor="10DG090092739", numero_chasis="935SLNFP0KB506813", uso="PARTICULAR")
    db.add(v3)
    db.flush()
    db.add(Poliza(id=str(uuid.uuid4()), cliente_id=c1.id, vehiculo_id=v3.id, numero_poliza="2514460-V3", compania="NACION SEGUROS", ramo="AUTOMOTORES", tipo_cobertura="CN C", fecha_inicio=datetime(2025, 10, 27).date(), fecha_vencimiento=datetime(2026, 10, 27).date(), suma_asegurada=Decimal("20000000"), premio_total=Decimal("38661.51"), estado="vigente"))
    
    v4 = Vehiculo(id=str(uuid.uuid4()), cliente_id=c2.id, dominio="AA977VD", tipo_vehiculo="AUTO", marca="VOLKSWAGEN", modelo="VENTO 1.4 TSI", anio=2017, numero_motor="CZD624375", numero_chasis="3VWVP6163HMD10230", uso="PARTICULAR")
    db.add(v4)
    db.flush()
    db.add(Poliza(id=str(uuid.uuid4()), cliente_id=c2.id, vehiculo_id=v4.id, numero_poliza="2506340", compania="NACION SEGUROS", ramo="AUTOMOTORES", tipo_cobertura="TODO RIESGO", fecha_inicio=datetime(2025, 10, 9).date(), fecha_vencimiento=datetime(2026, 10, 9).date(), suma_asegurada=Decimal("26180000"), premio_total=Decimal("65591.35"), estado="vigente"))
    
    v5 = Vehiculo(id=str(uuid.uuid4()), cliente_id=c1.id, dominio="AF523WE", tipo_vehiculo="AUTO", marca="TOYOTA", modelo="YARIS 1.5 CVT", anio=2022, numero_motor="2NR4613992", numero_chasis="9BRKB3F30P8198637", uso="PARTICULAR")
    db.add(v5)
    db.flush()
    db.add(Poliza(id=str(uuid.uuid4()), cliente_id=c1.id, vehiculo_id=v5.id, numero_poliza="2514552", compania="NACION SEGUROS", ramo="AUTOMOTORES", tipo_cobertura="TODO RIESGO", fecha_inicio=datetime(2025, 10, 25).date(), fecha_vencimiento=datetime(2026, 10, 25).date(), suma_asegurada=Decimal("28380000"), premio_total=Decimal("62377.25"), estado="vigente"))
    
    v6 = Vehiculo(id=str(uuid.uuid4()), cliente_id=c3.id, dominio="AE697PI", tipo_vehiculo="AUTO", marca="TOYOTA", modelo="COROLLA 2.0 CVT", anio=2021, numero_motor="M20AAA55707", numero_chasis="9BRB43BE0M2054652", uso="PARTICULAR")
    db.add(v6)
    db.flush()
    db.add(Poliza(id=str(uuid.uuid4()), cliente_id=c3.id, vehiculo_id=v6.id, numero_poliza="2513130", compania="NACION SEGUROS", ramo="AUTOMOTORES", tipo_cobertura="TODO RIESGO", fecha_inicio=datetime(2025, 10, 9).date(), fecha_vencimiento=datetime(2026, 10, 9).date(), suma_asegurada=Decimal("15180000"), premio_total=Decimal("41476.51"), estado="vigente"))
    
    v7 = Vehiculo(id=str(uuid.uuid4()), cliente_id=c1.id, dominio="AG937YQ", tipo_vehiculo="AUTO", marca="TOYOTA", modelo="COROLLA CROSS 2.0", anio=2024, numero_motor="M20AAE18867", numero_chasis="9BRK4AAGXS0163149", uso="PARTICULAR")
    db.add(v7)
    db.flush()
    db.add(Poliza(id=str(uuid.uuid4()), cliente_id=c1.id, vehiculo_id=v7.id, numero_poliza="2513311", compania="NACION SEGUROS", ramo="AUTOMOTORES", tipo_cobertura="TODO RIESGO", fecha_inicio=datetime(2025, 11, 3).date(), fecha_vencimiento=datetime(2026, 11, 3).date(), suma_asegurada=Decimal("50270000"), premio_total=Decimal("86346.49"), estado="vigente"))
    
    db.commit()
    
    return {
        "mensaje": "Datos reales cargados exitosamente",
        "usuario": "aybatista@icloud.com",
        "clientes": 3,
        "vehiculos": 7,
        "polizas": 7
    }
