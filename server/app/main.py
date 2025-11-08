"""
Punto de entrada principal de la aplicación FastAPI.
Configura la aplicación y todos sus componentes.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings, validate_settings
from app.api.routes import api_router


def create_app() -> FastAPI:
    """
    Factory function para crear la aplicación FastAPI.
    Sigue el principio de Dependency Inversion.
    Valida la configuración al inicio para asegurar seguridad.
    
    Returns:
        Instancia configurada de FastAPI
        
    Raises:
        RuntimeError: Si la configuración no es válida
    """
    # Validar configuración al inicio (incluye validación de API key)
    try:
        validate_settings()
    except Exception as e:
        raise RuntimeError(
            f"Error de configuración al iniciar la aplicación: {str(e)}. "
            "Por favor, verifica tu archivo .env y asegúrate de que GEMINI_API_KEY esté configurada correctamente."
        )
    
    app = FastAPI(
        title=settings.API_TITLE,
        version=settings.API_VERSION,
        description="API para generación de contenido educativo usando Gemini"
    )
    
    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Incluir routers
    app.include_router(api_router, prefix=settings.API_PREFIX)
    
    # Rutas básicas
    @app.get("/")
    def read_root():
        return {"message": "EduApp API está funcionando"}
    
    @app.get("/health")
    def health_check():
        # No exponer información sensible en el health check
        return {
            "status": "ok",
            "version": settings.API_VERSION,
            "gemini_configured": settings.is_gemini_configured
        }
    
    return app


# Crear instancia de la aplicación
app = create_app()

