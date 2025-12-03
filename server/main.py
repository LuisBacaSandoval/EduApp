"""
Punto de entrada del servidor.
Ejecuta la aplicación FastAPI usando uvicorn.
"""
from app.core.config import settings
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",  # String de importación para habilitar reload
        host=settings.HOST,
        port=settings.PORT,
        reload=True  # Activa el modo desarrollo con recarga automática
    )

