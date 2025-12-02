"""
Módulo de rutas de la API.
Centraliza la importación de todos los routers.
"""
from app.api.routes import teoria, pdf, recomendaciones, tutor
from fastapi import APIRouter

# Crear router principal
api_router = APIRouter()

# Incluir todos los routers
api_router.include_router(teoria.router)
api_router.include_router(pdf.router)
api_router.include_router(recomendaciones.router)
api_router.include_router(tutor.router)

__all__ = ["api_router"]
