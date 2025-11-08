"""
Servicio para interactuar con la API de Gemini.
Sigue el principio de Single Responsibility: solo maneja la comunicación con Gemini.
"""
from typing import Optional
from google import genai
from app.core.exceptions import GeminiServiceError


class GeminiService:
    """
    Servicio para interactuar con Google Gemini.
    Abstrae la lógica de comunicación con el LLM.
    """
    
    def __init__(self, api_key: Optional[str], model: str):
        """
        Inicializa el servicio de Gemini.
        
        Args:
            api_key: API key de Gemini (obtenida de settings)
            model: Modelo de Gemini a utilizar (obtenido de settings)
        """
        if not api_key:
            raise GeminiServiceError("API key de Gemini no configurada")
        
        self.client = genai.Client(api_key=api_key)
        self.model = model
    
    def generate_content(self, prompt: str) -> str:
        """
        Genera contenido usando Gemini.
        
        Args:
            prompt: El prompt a enviar a Gemini
            
        Returns:
            El texto generado por Gemini
            
        Raises:
            GeminiServiceError: Si hay un error al generar el contenido
        """
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text
        except Exception as e:
            raise GeminiServiceError(f"Error al generar contenido con Gemini: {str(e)}")
    
    def generate_theory(self, tema: str) -> str:
        """
        Genera teoría educativa sobre un tema dado.
        
        Args:
            tema: El tema sobre el cual generar teoría
            
        Returns:
            La teoría generada
        """
        prompt = (
            f"Genera una explicación teórica completa y educativa sobre el siguiente tema: {tema}. "
            f"Incluye conceptos clave, ejemplos cuando sea apropiado, y estructura la información "
            f"de manera clara y didáctica."
        )
        return self.generate_content(prompt)
    
    def generate_questions_from_text(self, texto: str) -> str:
        """
        Genera preguntas educativas basadas en un texto.
        
        Args:
            texto: El texto del cual generar preguntas
            
        Returns:
            Las preguntas generadas
        """
        prompt = (
            f"Basándote en el siguiente contenido, genera preguntas educativas y relevantes sobre el tema. "
            f"Las preguntas deben ser claras, variadas (de comprensión, análisis, aplicación) y útiles "
            f"para evaluar el aprendizaje. Genera entre 5 y 10 preguntas.\n\n"
            f"Contenido:\n{texto}"
        )
        return self.generate_content(prompt)

