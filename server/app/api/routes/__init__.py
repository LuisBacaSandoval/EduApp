"""
Módulo de rutas de la API.
Centraliza la importación de todos los routers.
"""
from app.api.routes import teoria, pdf
from fastapi import APIRouter

# Crear router principal
api_router = APIRouter()

# Incluir todos los routers
api_router.include_router(teoria.router)
api_router.include_router(pdf.router)

__all__ = ["api_router"]
