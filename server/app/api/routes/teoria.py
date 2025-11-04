"""
Rutas para la generación de teoría.
Sigue el principio de Single Responsibility: solo maneja las rutas relacionadas con teoría.
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import TheoryRequest, TheoryResponse
from app.services.gemini_service import GeminiService
from app.core.dependencies import get_gemini_service
from app.core.exceptions import GeminiServiceError

router = APIRouter(prefix="/teoria", tags=["teoría"])


@router.post("/generar", response_model=TheoryResponse)
async def generar_teoria(
    request: TheoryRequest,
    gemini_service: Optional[GeminiService] = Depends(get_gemini_service)
):
    """
    Genera teoría educativa sobre un tema dado usando Gemini.
    
    Args:
        request: Solicitud con el tema
        gemini_service: Servicio de Gemini (inyectado)
        
    Returns:
        Respuesta con la teoría generada
        
    Raises:
        HTTPException: Si hay un error al generar la teoría
    """
    if not gemini_service:
        raise HTTPException(
            status_code=500,
            detail="API key de Gemini no configurada. Por favor, configura GEMINI_API_KEY en el archivo .env"
        )
    
    try:
        teoria = gemini_service.generate_theory(request.tema)
        
        return TheoryResponse(
            tema=request.tema,
            teoria=teoria,
            success=True
        )
    except GeminiServiceError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado al generar teoría: {str(e)}"
        )

