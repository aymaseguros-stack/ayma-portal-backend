"""
Servicio de PDFs
Por ahora retorna URL mock, después se puede implementar generación real
"""
import os
from app.core.config import settings


def generar_url_poliza_pdf(numero_poliza: str) -> str:
    """
    Generar URL para PDF de póliza
    Por ahora retorna URL mock
    
    TODO: Implementar generación real de PDF con reportlab o weasyprint
    """
    # En producción, esto generaría el PDF y lo subiría a storage
    # Por ahora retornamos URL mock
    return f"{settings.FRONTEND_URL}/api/pdfs/poliza/{numero_poliza}.pdf"


def verificar_pdf_existe(url: str) -> bool:
    """
    Verificar si un PDF existe
    """
    if settings.STORAGE_TYPE == "local":
        # Extraer path del archivo de la URL
        filename = url.split('/')[-1]
        filepath = os.path.join(settings.STORAGE_PATH, filename)
        return os.path.exists(filepath)
    else:
        # Para S3 u otro storage, implementar verificación
        return False


def obtener_path_pdf_local(numero_poliza: str) -> str:
    """
    Obtener path local del PDF
    """
    filename = f"poliza_{numero_poliza}.pdf"
    return os.path.join(settings.STORAGE_PATH, filename)


# TODO: Implementar funciones reales de generación de PDF
# def generar_pdf_poliza(poliza_data: dict) -> bytes:
#     """Generar PDF de póliza con reportlab"""
#     pass
# 
# def guardar_pdf_storage(pdf_bytes: bytes, filename: str) -> str:
#     """Guardar PDF en storage y retornar URL"""
#     pass
