"""
Rutas para el procesamiento de PDFs y generación de preguntas.
Sigue el principio de Single Responsibility: solo maneja las rutas relacionadas con PDFs.
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from app.models.schemas import PDFQuestionsResponse, QuestionsStructured, TopicQuestionsRequest, TopicQuestionsResponse
from app.services.gemini_service import GeminiService
from app.services.pdf_service import PDFService
from app.core.dependencies import get_gemini_service, get_pdf_service
from app.core.exceptions import PDFServiceError, GeminiServiceError

import json

router = APIRouter(prefix="/pdf", tags=["pdf"])


@router.post("/generar-preguntas", response_model=PDFQuestionsResponse)
async def generar_preguntas_pdf(
    file: UploadFile = File(...),
    gemini_service: Optional[GeminiService] = Depends(get_gemini_service),
    pdf_service: PDFService = Depends(get_pdf_service)
):
    """
    Genera preguntas educativas basadas en el contenido de un PDF usando Gemini.
    
    Args:
        file: Archivo PDF a procesar
        gemini_service: Servicio de Gemini (inyectado)
        pdf_service: Servicio de PDF (inyectado)
        
    Returns:
        Respuesta con las preguntas generadas
        
    Raises:
        HTTPException: Si hay un error al procesar el PDF o generar preguntas
    """
    if not gemini_service:
        raise HTTPException(
            status_code=500,
            detail="API key de Gemini no configurada. Por favor, configura GEMINI_API_KEY en el archivo .env"
        )
    
    # Validar que el archivo sea un PDF
    if not pdf_service.validate_pdf_content_type(file.content_type):
        raise HTTPException(
            status_code=400,
            detail="El archivo debe ser un PDF (application/pdf)"
        )
    
    try:
        # Leer el contenido del archivo
        pdf_content = await file.read()
        
        # Extraer texto del PDF
        texto_pdf = pdf_service.extract_text(pdf_content)
        
        # Generar preguntas usando Gemini
        preguntas = gemini_service.generate_questions_from_text(texto_pdf)

        if not preguntas or preguntas.strip() == "":
            raise HTTPException(
                status_code=500,
                detail="El servicio de Gemini no devolvió contenido"
            )
        
        if preguntas.startswith("```json"):
            preguntas = preguntas.replace("```json", "")
        if preguntas.endswith("```"):
            preguntas = preguntas.replace("```", "")

        data = json.loads(preguntas)
        
        return PDFQuestionsResponse(**data)
    
    except (PDFServiceError, GeminiServiceError) as e:
        raise HTTPException(
            status_code=400 if isinstance(e, PDFServiceError) else 500,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado al procesar PDF: {str(e)}"
        )


@router.post("/generar-preguntas-por-tema", response_model=TopicQuestionsResponse)
async def generar_preguntas_por_tema(
    request: TopicQuestionsRequest,
    gemini_service: Optional[GeminiService] = Depends(get_gemini_service)
):
    """
    Genera preguntas educativas basadas en un tema específico usando Gemini.
    Similar al endpoint de PDF pero recibe un tema en lugar de un archivo.
    Usa la misma estructura de respuesta que el endpoint de PDF.
    
    Args:
        request: Solicitud con el tema y cantidad de preguntas
        gemini_service: Servicio de Gemini (inyectado)
        
    Returns:
        Respuesta con las preguntas generadas (mismo formato que PDF)
        
    Raises:
        HTTPException: Si hay un error al generar las preguntas
        
    Example:
        POST /api/pdf/generar-preguntas-por-tema
        {
            "tema": "La fotosíntesis",
            "cantidad": 5
        }
    """
    if not gemini_service:
        raise HTTPException(
            status_code=500,
            detail="API key de Gemini no configurada. Por favor, configura GEMINI_API_KEY en el archivo .env"
        )
    
    try:
        # Generar preguntas usando Gemini
        preguntas_str = gemini_service.generate_questions_from_topic(
            tema=request.tema,
            cantidad=request.cantidad
        )
        
        if not preguntas_str or preguntas_str.strip() == "":
            raise HTTPException(
                status_code=500,
                detail="El servicio de Gemini no devolvió contenido"
            )
        
        # Limpiar markdown si existe
        if preguntas_str.startswith("```json"):
            preguntas_str = preguntas_str.replace("```json", "")
        if preguntas_str.endswith("```"):
            preguntas_str = preguntas_str.replace("```", "")
        
        # Parsear JSON
        try:
            data = json.loads(preguntas_str)
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al parsear la respuesta de Gemini: {str(e)}"
            )
        
        # Validar que haya questions
        if not data.get("questions"):
            raise HTTPException(
                status_code=500,
                detail="No se generaron preguntas"
            )
        
        # Re-indexar las preguntas para asegurar que empiecen en 0
        for index, question in enumerate(data["questions"]):
            question["id"] = index
        
        # Validar estructura con Pydantic
        return TopicQuestionsResponse(
            questions=data["questions"],
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
            detail=f"Error inesperado al generar preguntas: {str(e)}"
        )

