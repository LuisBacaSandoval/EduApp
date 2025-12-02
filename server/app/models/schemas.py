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

class Question(BaseModel):
    """Schema para una pregunta de opción múltiple."""
    id: int
    content: str
    possibleAnswers: list[str]
    correctAnswer: int

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
    questions: list[Question]


class TopicQuestionsRequest(BaseModel):
    """Schema para la solicitud de generación de preguntas por tema."""
    tema: str = Field(
        ..., 
        min_length=1, 
        max_length=500, 
        description="Tema sobre el cual generar preguntas"
    )
    cantidad: int = Field(
        default=5,
        ge=3,
        le=10,
        description="Cantidad de preguntas a generar (3-10)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "tema": "La fotosíntesis en las plantas",
                "cantidad": 5
            }
        }


class TopicQuestionsResponse(BaseModel):
    """Schema para la respuesta de generación de preguntas por tema."""
    questions: list[Question]
    success: bool = True
    
    class Config:
        json_schema_extra = {
            "example": {
                "questions": [
                    {
                        "id": 0,
                        "content": "¿Qué es la fotosíntesis?",
                        "possibleAnswers": [
                            "Proceso de respiración",
                            "Proceso de conversión de luz en energía",
                            "Proceso de crecimiento",
                            "Proceso de absorción de agua"
                        ],
                        "correctAnswer": 1
                    }
                ],
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


# Schemas para recomendaciones de temas aleatorios
class RandomTopicsResponse(BaseModel):
    """Schema para la respuesta de temas aleatorios (solo títulos)."""
    temas: List[str] = Field(..., description="Lista de títulos de temas recomendados")
    success: bool = True
    
    class Config:
        json_schema_extra = {
            "example": {
                "temas": [
                    "Geometría Fractal",
                    "Revolución Industrial",
                    "Inteligencia Artificial"
                ],
                "success": True
            }
        }


# Schemas para tutor virtual
class TutorInitRequest(BaseModel):
    """Schema para iniciar una conversación con el tutor."""
    tema: str = Field(
        ..., 
        min_length=1, 
        max_length=500, 
        description="Tema sobre el cual el tutor será experto"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "tema": "La Segunda Guerra Mundial"
            }
        }


class Message(BaseModel):
    """Schema para un mensaje en la conversación."""
    role: str = Field(..., description="Rol: 'user' o 'tutor'")
    content: str = Field(..., description="Contenido del mensaje")
    timestamp: Optional[str] = Field(None, description="Timestamp del mensaje")


class TutorMessageRequest(BaseModel):
    """Schema para enviar un mensaje al tutor."""
    tema: str = Field(
        ..., 
        min_length=1, 
        max_length=500, 
        description="Tema de la conversación (debe coincidir con el tema inicial)"
    )
    mensaje: str = Field(
        ..., 
        min_length=1, 
        max_length=1000, 
        description="Mensaje del usuario al tutor"
    )
    historial: List[Message] = Field(
        default_factory=list,
        description="Historial de la conversación (para mantener contexto)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "tema": "La Segunda Guerra Mundial",
                "mensaje": "¿Cuándo comenzó la guerra?",
                "historial": [
                    {
                        "role": "tutor",
                        "content": "Hola, soy UNIprofe y soy experto en La Segunda Guerra Mundial...",
                        "timestamp": "2024-01-01T10:00:00"
                    }
                ]
            }
        }


class TutorInitResponse(BaseModel):
    """Schema para la respuesta inicial del tutor."""
    mensaje: str = Field(..., description="Mensaje de presentación del tutor")
    tema: str = Field(..., description="Tema sobre el cual es experto")
    success: bool = True
    
    class Config:
        json_schema_extra = {
            "example": {
                "mensaje": "Hola 👋, soy UNIprofe y soy experto en La Segunda Guerra Mundial. Estoy aquí para ayudarte en todas tus dudas sobre este tema. ¿Qué es lo que deseas saber?",
                "tema": "La Segunda Guerra Mundial",
                "success": True
            }
        }


class TutorMessageResponse(BaseModel):
    """Schema para la respuesta del tutor a un mensaje."""
    respuesta: str = Field(..., description="Respuesta del tutor")
    tema: str = Field(..., description="Tema de la conversación")
    success: bool = True
    
    class Config:
        json_schema_extra = {
            "example": {
                "respuesta": "La Segunda Guerra Mundial comenzó el 1 de septiembre de 1939...",
                "tema": "La Segunda Guerra Mundial",
                "success": True
            }
        }

