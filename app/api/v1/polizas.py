"""
Endpoints de Pólizas
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Cliente, Poliza
from app.schemas.poliza import PolizaResponse, PolizaResumen, PolizaCreate
from app.services import scoring as scoring_service
from app.api.dependencies import get_current_cliente, require_admin

router = APIRouter(prefix="/polizas", tags=["Pólizas"])


@router.get("/", response_model=List[PolizaResumen])
def listar_polizas_cliente(
    cliente: Cliente = Depends(get_current_cliente),
    db: Session = Depends(get_db)
):
    """
    Listar todas las pólizas del cliente autenticado
    """
    polizas = db.query(Poliza).filter(
        Poliza.cliente_id == cliente.id
    ).order_by(Poliza.fecha_vencimiento.desc()).all()
    
    # Registrar actividad
    scoring_service.registrar_actividad(
        db,
        cliente_id=cliente.id,
        tipo_actividad="ver_poliza",
        descripcion="Listado de pólizas"
    )
    
    return polizas


@router.get("/{poliza_id}", response_model=PolizaResponse)
def obtener_poliza(
    poliza_id: str,
    cliente: Cliente = Depends(get_current_cliente),
    db: Session = Depends(get_db)
):
    """
    Obtener detalle de una póliza específica
    """
    poliza = db.query(Poliza).filter(
        Poliza.id == poliza_id,
        Poliza.cliente_id == cliente.id
    ).first()
    
    if not poliza:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Póliza no encontrada"
        )
    
    # Registrar actividad
    scoring_service.registrar_actividad(
        db,
        cliente_id=cliente.id,
        tipo_actividad="ver_poliza",
        descripcion=f"Vio detalle de póliza {poliza.numero_poliza}"
    )
    
    return poliza


@router.get("/{poliza_id}/pdf")
def descargar_pdf_poliza(
    poliza_id: str,
    cliente: Cliente = Depends(get_current_cliente),
    db: Session = Depends(get_db)
):
    """
    Descargar PDF de la póliza
    """
    poliza = db.query(Poliza).filter(
        Poliza.id == poliza_id,
        Poliza.cliente_id == cliente.id
    ).first()
    
    if not poliza:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Póliza no encontrada"
        )
    
    # Registrar actividad
    scoring_service.registrar_actividad(
        db,
        cliente_id=cliente.id,
        tipo_actividad="descargar_pdf",
        descripcion=f"Descargó PDF de póliza {poliza.numero_poliza}"
    )
    
    # Por ahora retornar URL mock
    # TODO: Implementar descarga real de PDF
    return {
        "url": poliza.url_poliza_pdf or f"/api/pdfs/poliza_{poliza.numero_poliza}.pdf",
        "numero_poliza": poliza.numero_poliza,
        "message": "Mock PDF URL - Implementar generación/descarga real"
    }


@router.post("/", response_model=PolizaResponse)
def crear_poliza(
    poliza_data: PolizaCreate,
    db: Session = Depends(get_db),
    admin = Depends(require_admin)
):
    """
    Crear nueva póliza (solo admin)
    """
    # Verificar que el cliente existe
    cliente = db.query(Cliente).filter(Cliente.id == poliza_data.cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )
    
    # Verificar que no exista otra póliza con ese número
    existing = db.query(Poliza).filter(
        Poliza.numero_poliza == poliza_data.numero_poliza
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una póliza con ese número"
        )
    
    # Crear póliza
    poliza = Poliza(**poliza_data.model_dump())
    db.add(poliza)
    
    # Actualizar contador de pólizas del cliente
    cliente.cantidad_polizas += 1
    
    db.commit()
    db.refresh(poliza)
    
    return poliza
