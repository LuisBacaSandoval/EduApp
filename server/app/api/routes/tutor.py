"""
Rutas para el tutor virtual.
Sigue el principio de Single Responsibility: solo maneja las rutas relacionadas con el tutor.
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import (
    TutorInitRequest,
    TutorInitResponse,
    TutorMessageRequest,
    TutorMessageResponse,
    Message
)
from app.services.gemini_service import GeminiService
from app.core.dependencies import get_gemini_service
from app.core.exceptions import GeminiServiceError

router = APIRouter(prefix="/tutor", tags=["tutor"])


@router.post("/iniciar", response_model=TutorInitResponse)
async def iniciar_tutor(
    request: TutorInitRequest,
    gemini_service: Optional[GeminiService] = Depends(get_gemini_service)
):
    """
    Inicia una conversación con el tutor virtual.
    El tutor se presenta como experto en el tema especificado.
    
    Args:
        request: Solicitud con el tema
        gemini_service: Servicio de Gemini (inyectado)
        
    Returns:
        Mensaje de presentación del tutor
        
    Raises:
        HTTPException: Si hay un error al generar la presentación
        
    Example:
        POST /api/tutor/iniciar
        {
            "tema": "La Segunda Guerra Mundial"
        }
    """
    if not gemini_service:
        raise HTTPException(
            status_code=500,
            detail="API key de Gemini no configurada. Por favor, configura GEMINI_API_KEY en el archivo .env"
        )
    
    try:
        # Generar mensaje de presentación
        mensaje = gemini_service.generate_tutor_introduction(request.tema)
        
        if not mensaje or mensaje.strip() == "":
            raise HTTPException(
                status_code=500,
                detail="No se pudo generar el mensaje del tutor"
            )
        
        return TutorInitResponse(
            mensaje=mensaje.strip(),
            tema=request.tema,
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
            detail=f"Error inesperado al iniciar tutor: {str(e)}"
        )


@router.post("/mensaje", response_model=TutorMessageResponse)
async def enviar_mensaje_tutor(
    request: TutorMessageRequest,
    gemini_service: Optional[GeminiService] = Depends(get_gemini_service)
):
    """
    Envía un mensaje al tutor y recibe una respuesta.
    Mantiene el contexto de la conversación mediante el historial.
    
    Args:
        request: Solicitud con mensaje, tema e historial
        gemini_service: Servicio de Gemini (inyectado)
        
    Returns:
        Respuesta del tutor
        
    Raises:
        HTTPException: Si hay un error al generar la respuesta
        
    Example:
        POST /api/tutor/mensaje
        {
            "tema": "La Segunda Guerra Mundial",
            "mensaje": "¿Cuándo comenzó la guerra?",
            "historial": [...]
        }
    """
    if not gemini_service:
        raise HTTPException(
            status_code=500,
            detail="API key de Gemini no configurada. Por favor, configura GEMINI_API_KEY en el archivo .env"
        )
    
    # Validar que el mensaje no esté vacío
    if not request.mensaje or not request.mensaje.strip():
        raise HTTPException(
            status_code=400,
            detail="El mensaje no puede estar vacío"
        )
    
    try:
        # Convertir historial a formato dict si viene como objetos Message
        historial_dict = []
        for msg in request.historial:
            if isinstance(msg, Message):
                historial_dict.append({
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp
                })
            elif isinstance(msg, dict):
                historial_dict.append(msg)
        
        # Generar respuesta del tutor
        respuesta = gemini_service.generate_tutor_response(
            tema=request.tema,
            mensaje_usuario=request.mensaje.strip(),
            historial=historial_dict
        )
        
        if not respuesta or respuesta.strip() == "":
            raise HTTPException(
                status_code=500,
                detail="No se pudo generar la respuesta del tutor"
            )
        
        return TutorMessageResponse(
            respuesta=respuesta.strip(),
            tema=request.tema,
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
            detail=f"Error inesperado al procesar mensaje: {str(e)}"
        )

