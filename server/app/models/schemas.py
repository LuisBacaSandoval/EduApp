"""
Schemas de Pydantic para validación de datos.
Define los modelos de entrada y salida de la API.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class TheoryRequest(BaseModel):
    """Schema para la solicitud de generación de teoría."""
    tema: str = Field(..., min_length=1, max_length=500, description="Tema sobre el cual generar teoría")

    class Config:
        json_schema_extra = {
            "example": {
                "tema": "La fotosíntesis en las plantas"
            }
        }


# Schemas para teoría estructurada
class SeccionTeoria(BaseModel):
    """Schema para una sección de teoría."""
    titulo: str = Field(..., description="Título de la sección")
    contenido: str = Field(..., description="Contenido de la sección")


class TheoryStructured(BaseModel):
    """Schema para la teoría estructurada generada por Gemini."""
    titulo: str = Field(..., description="Título principal del tema")
    introduccion: str = Field(..., description="Introducción al tema")
    secciones: List[SeccionTeoria] = Field(..., description="Lista de secciones de la teoría")
    conceptos_clave: List[str] = Field(default_factory=list, description="Lista de conceptos clave")
    ejemplos: Optional[List[str]] = Field(default=None, description="Ejemplos relacionados")


class TheoryResponse(BaseModel):
    """Schema para la respuesta de generación de teoría."""
    tema: str
    teoria: TheoryStructured
    success: bool = True

    class Config:
        json_schema_extra = {
            "example": {
                "tema": "La fotosíntesis en las plantas",
                "teoria": {
                    "titulo": "La Fotosíntesis",
                    "introduccion": "La fotosíntesis es...",
                    "secciones": [
                        {
                            "titulo": "Proceso de la fotosíntesis",
                            "contenido": "El proceso consiste en..."
                        }
                    ],
                    "conceptos_clave": ["clorofila", "dióxido de carbono"],
                    "ejemplos": ["Plantas verdes", "Algas"]
                },
                "success": True
            }
        }


# Schemas para preguntas estructuradas
class Pregunta(BaseModel):
    """Schema para una pregunta individual."""
    numero: int = Field(..., description="Número de la pregunta")
    pregunta: str = Field(..., description="Texto de la pregunta")
    opciones: List[str] = Field(..., min_items=4, max_items=4, description="Opciones de respuesta (A, B, C, D)")
    respuesta_correcta: str = Field(..., description="Letra de la respuesta correcta (A, B, C o D)")
    tipo: str = Field(..., description="Tipo de pregunta: comprension, analisis, o aplicacion")
    dificultad: Optional[str] = Field(default="media", description="Dificultad: facil, media, o alta")


class QuestionsStructured(BaseModel):
    """Schema para las preguntas estructuradas generadas por Gemini."""
    preguntas: List[Pregunta] = Field(..., description="Lista de preguntas generadas")


class PDFQuestionsResponse(BaseModel):
    """Schema para la respuesta de generación de preguntas desde PDF."""
    nombre_archivo: str
    preguntas: QuestionsStructured
    success: bool = True

    class Config:
        json_schema_extra = {
            "example": {
                "nombre_archivo": "documento.pdf",
                "preguntas": {
                    "preguntas": [
                        {
                            "numero": 1,
                            "pregunta": "¿Cuál es el tema principal?",
                            "opciones": ["Opción A", "Opción B", "Opción C", "Opción D"],
                            "respuesta_correcta": "A",
                            "tipo": "comprension",
                            "dificultad": "facil"
                        }
                    ]
                },
                "success": True
            }
        }


class ErrorResponse(BaseModel):
    """Schema para respuestas de error."""
    detail: str
    success: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Error al procesar la solicitud",
                "success": False
            }
        }

