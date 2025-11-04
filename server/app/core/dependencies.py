"""
Dependencias de la aplicación.
Implementa Dependency Injection para seguir el principio de Dependency Inversion.
"""
from typing import Optional
from app.services.gemini_service import GeminiService
from app.services.pdf_service import PDFService
from app.core.config import settings
from app.core.exceptions import GeminiServiceError


def get_gemini_service() -> Optional[GeminiService]:
    """
    Factory function para obtener el servicio de Gemini.
    Permite inyección de dependencias y facilita testing.
    Usa get_gemini_api_key() para obtener la key de forma segura.
    Retorna None si no está configurado (para validar en las rutas).
    """
    if not settings.is_gemini_configured:
        return None
    try:
        # Usar get_gemini_api_key() para obtener la key de forma segura
        api_key = settings.get_gemini_api_key()
        return GeminiService(api_key=api_key, model=settings.GEMINI_MODEL)
    except GeminiServiceError:
        return None
    except Exception as e:
        # No exponer detalles del error que puedan incluir la API key
        raise GeminiServiceError("Error al inicializar el servicio de Gemini")


def get_pdf_service() -> PDFService:
    """
    Factory function para obtener el servicio de PDF.
    Permite inyección de dependencias y facilita testing.
    """
    return PDFService(max_text_length=settings.MAX_PDF_TEXT_LENGTH)

