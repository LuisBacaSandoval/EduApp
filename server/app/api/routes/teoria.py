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
    """
    Convierte un objeto TheoryStructured a HTML formateado.
    
    Args:
        tema: El tema de la teoría
        teoria: Objeto TheoryStructured con la teoría
        
    Returns:
        String con HTML formateado
    """
    # Generar HTML para las secciones
    secciones_html = ""
    for seccion in teoria.secciones:
        secciones_html += f"""
        <section class="seccion">
            <h2>{seccion.titulo}</h2>
            <p>{seccion.contenido}</p>
        </section>
        """
    
    # Generar HTML para conceptos clave
    conceptos_html = ""
    if teoria.conceptos_clave:
        conceptos_items = "".join([f"<li>{concepto}</li>" for concepto in teoria.conceptos_clave])
        conceptos_html = f"""
        <div class="conceptos-clave">
            <h2>Conceptos Clave</h2>
            <ul>
                {conceptos_items}
            </ul>
        </div>
        """
    
    # Generar HTML para ejemplos
    ejemplos_html = ""
    if teoria.ejemplos:
        ejemplos_items = "".join([f"<li>{ejemplo}</li>" for ejemplo in teoria.ejemplos])
        ejemplos_html = f"""
        <div class="ejemplos">
            <h2>Ejemplos</h2>
            <ul>
                {ejemplos_items}
            </ul>
        </div>
        """
    
    # HTML completo
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{teoria.titulo}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
                color: #333;
            }}
            .container {{
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }}
            .tema {{
                background-color: #ecf0f1;
                padding: 10px 15px;
                border-left: 4px solid #3498db;
                margin-bottom: 20px;
                font-style: italic;
            }}
            .introduccion {{
                background-color: #e8f4f8;
                padding: 20px;
                border-radius: 5px;
                margin-bottom: 30px;
                border-left: 4px solid #3498db;
            }}
            .seccion {{
                margin-bottom: 30px;
            }}
            .seccion h2 {{
                color: #34495e;
                margin-bottom: 10px;
                border-bottom: 2px solid #ecf0f1;
                padding-bottom: 5px;
            }}
            .seccion p {{
                text-align: justify;
                line-height: 1.8;
            }}
            .conceptos-clave, .ejemplos {{
                background-color: #fff9e6;
                padding: 20px;
                border-radius: 5px;
                margin-top: 30px;
                border-left: 4px solid #f39c12;
            }}
            .conceptos-clave h2, .ejemplos h2 {{
                color: #e67e22;
                margin-top: 0;
            }}
            ul {{
                list-style-type: none;
                padding-left: 0;
            }}
            li {{
                padding: 8px 0;
                padding-left: 25px;
                position: relative;
            }}
            li:before {{
                content: "▸";
                position: absolute;
                left: 0;
                color: #3498db;
                font-weight: bold;
            }}
            .conceptos-clave li:before {{
                color: #f39c12;
                content: "●";
            }}
            .footer {{
                margin-top: 40px;
                text-align: center;
                color: #7f8c8d;
                font-size: 0.9em;
                border-top: 1px solid #ecf0f1;
                padding-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{teoria.titulo}</h1>
            
            <div class="tema">
                <strong>Tema:</strong> {tema}
            </div>
            
            <div class="introduccion">
                <strong>Introducción:</strong><br>
                {teoria.introduccion}
            </div>
            
            {secciones_html}
            
            {conceptos_html}
            
            {ejemplos_html}
            
            <div class="footer">
                Generado por EduApp - Contenido educativo con IA
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content


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

