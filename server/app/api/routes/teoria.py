"""
Rutas para la generación de teoría.
Sigue el principio de Single Responsibility: solo maneja las rutas relacionadas con teoría.
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import HTMLResponse
from app.models.schemas import TheoryRequest, TheoryResponse, TheoryStructured
from app.services.gemini_service import GeminiService
from app.core.dependencies import get_gemini_service
from app.core.exceptions import GeminiServiceError

router = APIRouter(prefix="/teoria", tags=["teoría"])


def teoria_to_html(tema: str, teoria: TheoryStructured) -> str:
    secciones_html = ""
    for seccion in teoria.secciones:
        secciones_html += f"""
        <section class="mb-8">
            <h2 class="text-xl font-semibold text-gray-800 mb-2 border-b pb-1">{seccion.titulo}</h2>
            <p class="text-gray-700 leading-relaxed">{seccion.contenido}</p>
        </section>
        """

    conceptos_html = ""
    if teoria.conceptos_clave:
        conceptos_items = "".join(
            f'<li class="pl-4 relative before:content-[\'•\'] before:absolute before:left-0 before:text-blue-500">{c}</li>'
            for c in teoria.conceptos_clave
        )
        conceptos_html = f"""
        <div class="bg-yellow-50 p-4 rounded-lg mb-8">
            <h2 class="text-lg font-semibold text-yellow-600 mb-2">Conceptos Clave</h2>
            <ul class="space-y-1">
                {conceptos_items}
            </ul>
        </div>
        """

    ejemplos_html = ""
    if teoria.ejemplos:
        ejemplos_items = "".join(
            f'<li class="pl-4 relative before:content-[\'•\'] before:absolute before:left-0 before:text-green-500">{e}</li>'
            for e in teoria.ejemplos
        )
        ejemplos_html = f"""
        <div class="bg-blue-50 p-4 rounded-lg mb-8">
            <h2 class="text-lg font-semibold text-blue-600 mb-2">Ejemplos</h2>
            <ul class="space-y-1">
                {ejemplos_items}
            </ul>
        </div>
        """

    html_content = f"""
        <div class="max-w-3xl mx-auto bg-white rounded-xl shadow-md p-6">
            <h1 class="text-3xl font-bold text-gray-900 mb-4">{teoria.titulo}</h1>

            <div class="bg-gray-100 p-3 rounded-md mb-6">
                <strong class="font-medium">Tema:</strong> {tema}
            </div>

            <div class="bg-blue-50 p-4 rounded-lg mb-8 border-l-4 border-blue-400">
                <p class="text-gray-800">
                    <strong class="font-semibold">Introducción:</strong><br>
                    {teoria.introduccion}
                </p>
            </div>

            {secciones_html}
            {conceptos_html}
            {ejemplos_html}

            <div class="text-center text-sm text-gray-500 mt-8 pt-4 border-t">
                Generado por EduApp - Contenido educativo con IA
            </div>
        </div>
    """

    return html_content.strip()


@router.post("/generar", response_model=TheoryResponse)
async def generar_teoria(
    request: TheoryRequest,
    gemini_service: Optional[GeminiService] = Depends(get_gemini_service)
):
    """
    Genera teoría educativa sobre un tema dado usando Gemini.
    Responde en formato JSON.
    
    Args:
        request: Solicitud con el tema
        gemini_service: Servicio de Gemini (inyectado)
        
    Returns:
        Respuesta con la teoría generada en JSON
        
    Raises:
        HTTPException: Si hay un error al generar la teoría
    """
    if not gemini_service:
        raise HTTPException(
            status_code=500,
            detail="API key de Gemini no configurada. Por favor, configura GEMINI_API_KEY en el archivo .env"
        )
    
    try:
        teoria_dict = gemini_service.generate_theory(request.tema)
        
        # Validar y convertir el diccionario a TheoryStructured
        try:
            teoria_structured = TheoryStructured(**teoria_dict)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al validar la estructura de la teoría generada: {str(e)}"
            )
        
        return TheoryResponse(
            tema=request.tema,
            teoria=teoria_structured,
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
            detail=f"Error inesperado al generar teoría: {str(e)}"
        )


@router.post("/generar-html", response_class=HTMLResponse)
async def generar_teoria_html(
    request: TheoryRequest,
    gemini_service: Optional[GeminiService] = Depends(get_gemini_service)
):
    """
    Genera teoría educativa sobre un tema dado usando Gemini.
    Responde en formato HTML listo para visualizar.
    
    Args:
        request: Solicitud con el tema
        gemini_service: Servicio de Gemini (inyectado)
        
    Returns:
        Respuesta con la teoría generada en HTML formateado
        
    Raises:
        HTTPException: Si hay un error al generar la teoría
    """
    if not gemini_service:
        raise HTTPException(
            status_code=500,
            detail="API key de Gemini no configurada. Por favor, configura GEMINI_API_KEY en el archivo .env"
        )
    
    try:
        teoria_dict = gemini_service.generate_theory(request.tema)
        
        # Validar y convertir el diccionario a TheoryStructured
        try:
            teoria_structured = TheoryStructured(**teoria_dict)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al validar la estructura de la teoría generada: {str(e)}"
            )
        
        # Convertir a HTML
        html_content = teoria_to_html(request.tema, teoria_structured)
        
        return HTMLResponse(content=html_content, status_code=200)
        
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
            detail=f"Error inesperado al generar teoría: {str(e)}"
        )

