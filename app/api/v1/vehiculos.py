"""
Endpoints de Vehículos
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Cliente, Vehiculo, Poliza
from app.schemas.vehiculo import VehiculoResponse, VehiculoResumen
from app.api.dependencies import get_current_cliente

router = APIRouter(tags=["Vehículos"])


@router.get("/", response_model=List[VehiculoResumen])
def listar_vehiculos_cliente(
    cliente: Cliente = Depends(get_current_cliente),
    db: Session = Depends(get_db)
):
    """
    Listar todos los vehículos del cliente autenticado
    """
    vehiculos = db.query(Vehiculo).filter(
        Vehiculo.cliente_id == cliente.id
    ).all()
    
    # Agregar info de si tiene póliza vigente
    vehiculos_con_info = []
    for vehiculo in vehiculos:
        vehiculo_dict = {
            "id": vehiculo.id,
            "dominio": vehiculo.dominio,
            "descripcion_completa": vehiculo.descripcion_completa,
            "anio": vehiculo.anio,
            "estado": vehiculo.estado,
            "tiene_poliza_vigente": False
        }
        
        # Verificar si tiene póliza vigente
        poliza_vigente = db.query(Poliza).filter(
            Poliza.vehiculo_id == vehiculo.id,
            Poliza.estado == "vigente"
        ).first()
        
        if poliza_vigente:
            vehiculo_dict["tiene_poliza_vigente"] = True
        
        vehiculos_con_info.append(vehiculo_dict)
    
    return vehiculos_con_info


@router.get("/{vehiculo_id}", response_model=VehiculoResponse)
def obtener_vehiculo(
    vehiculo_id: str,
    cliente: Cliente = Depends(get_current_cliente),
    db: Session = Depends(get_db)
):
    """
    Obtener detalle de un vehículo específico
    """
    vehiculo = db.query(Vehiculo).filter(
        Vehiculo.id == vehiculo_id,
        Vehiculo.cliente_id == cliente.id
    ).first()
    
    if not vehiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehículo no encontrado"
        )
    
    return vehiculo


@router.get("/{vehiculo_id}/polizas")
def obtener_polizas_vehiculo(
    vehiculo_id: str,
    cliente: Cliente = Depends(get_current_cliente),
    db: Session = Depends(get_db)
):
    """
    Obtener pólizas asociadas a un vehículo
    """
    vehiculo = db.query(Vehiculo).filter(
        Vehiculo.id == vehiculo_id,
        Vehiculo.cliente_id == cliente.id
    ).first()
    
    if not vehiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehículo no encontrado"
        )
    
    polizas = db.query(Poliza).filter(
        Poliza.vehiculo_id == vehiculo_id
    ).order_by(Poliza.fecha_vencimiento.desc()).all()
    
    return polizas
