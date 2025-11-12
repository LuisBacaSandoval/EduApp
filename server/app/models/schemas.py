"""
Schemas de Pydantic para validación de datos.
Define los modelos de entrada y salida de la API.
"""
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


class TheoryResponse(BaseModel):
    """Schema para la respuesta de generación de teoría."""
    tema: str
    teoria: str
    success: bool = True

    class Config:
        json_schema_extra = {
            "example": {
                "tema": "La fotosíntesis en las plantas",
                "teoria": "La fotosíntesis es un proceso...",
                "success": True
            }
        }

class Question(BaseModel):
    """Schema para una pregunta de opción múltiple."""
    id: int
    content: str
    possibleAnswers: list[str]
    correctAnswer: str

class PDFQuestionsResponse(BaseModel):
    """Schema para la respuesta de generación de preguntas desde PDF."""
    questions: list[Question]


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

