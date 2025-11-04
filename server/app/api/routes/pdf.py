"""
Rutas para el procesamiento de PDFs y generación de preguntas.
Sigue el principio de Single Responsibility: solo maneja las rutas relacionadas con PDFs.
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from app.models.schemas import PDFQuestionsResponse
from app.services.gemini_service import GeminiService
from app.services.pdf_service import PDFService
from app.core.dependencies import get_gemini_service, get_pdf_service
from app.core.exceptions import PDFServiceError, GeminiServiceError

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
        
        return PDFQuestionsResponse(
            nombre_archivo=file.filename or "documento.pdf",
            preguntas=preguntas,
            success=True
        )
    
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

