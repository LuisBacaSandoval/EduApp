"""
Punto de entrada del servidor.
Ejecuta la aplicación FastAPI usando uvicorn.
"""
from app.main import app
from app.core.config import settings
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=True  # Activa el modo desarrollo con recarga automática
    )

