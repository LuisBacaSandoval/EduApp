"""
Rutas para la generación de temas recomendados aleatorios.
Sigue el principio de Single Responsibility: solo maneja las rutas relacionadas con recomendaciones.
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from app.models.schemas import RandomTopicsResponse
from app.services.gemini_service import GeminiService
from app.core.dependencies import get_gemini_service
from app.core.exceptions import GeminiServiceError

router = APIRouter(prefix="/recomendaciones", tags=["recomendaciones"])


@router.get("/aleatorias", response_model=RandomTopicsResponse)
async def generar_temas_aleatorios(
    cantidad: int = Query(default=3, ge=3, le=5, description="Cantidad de temas (3-5)"),
    gemini_service: Optional[GeminiService] = Depends(get_gemini_service)
):
    """
    Genera títulos de temas educativos completamente aleatorios.
    Cada llamada genera temas diferentes - ideal para mostrar recomendaciones en la UI.
    
    Args:
        cantidad: Cantidad de temas a generar (3-5, por defecto 3)
        gemini_service: Servicio de Gemini (inyectado)
        
    Returns:
        Lista de títulos de temas aleatorios
        
    Raises:
        HTTPException: Si hay un error al generar las recomendaciones
        
    Example:
        GET /api/recomendaciones/aleatorias
        GET /api/recomendaciones/aleatorias?cantidad=5
        
        Response:
        {
            "temas": ["Matemática Avanzada", "Física Cuántica", "Historia Medieval"],
            "success": true
        }
    """
    if not gemini_service:
        raise HTTPException(
            status_code=500,
            detail="API key de Gemini no configurada. Por favor, configura GEMINI_API_KEY en el archivo .env"
        )
    
    try:
        # Generar títulos aleatorios usando Gemini
        temas_dict = gemini_service.generate_random_topic_titles(cantidad=cantidad)
        
        # Validar que haya temas
        if not temas_dict.get("temas"):
            raise HTTPException(
                status_code=500,
                detail="No se pudieron generar temas"
            )
        
        temas_list = temas_dict["temas"]
        
        # Verificar que sean strings
        if not all(isinstance(tema, str) for tema in temas_list):
            raise HTTPException(
                status_code=500,
                detail="Error en el formato de los temas generados"
            )
        
        # Verificar cantidad
        if len(temas_list) < cantidad:
            raise HTTPException(
                status_code=500,
                detail=f"Se generaron {len(temas_list)} temas, pero se esperaban {cantidad}"
            )
        
        # Tomar solo la cantidad solicitada
        temas_list = temas_list[:cantidad]
        
        return RandomTopicsResponse(
            temas=temas_list,
            success=True
        )
        
    except GeminiServiceError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado al generar temas: {str(e)}"
        )

