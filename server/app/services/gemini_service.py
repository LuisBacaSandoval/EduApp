"""
Servicio para interactuar con la API de Gemini.
Sigue el principio de Single Responsibility: solo maneja la comunicación con Gemini.
"""
import json
import re
from typing import Optional, Dict, Any
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
    
    def _parse_json_from_text(self, text: str) -> Dict[str, Any]:
        """
        Intenta extraer y parsear JSON del texto generado por Gemini.
        
        Args:
            text: Texto que puede contener JSON
            
        Returns:
            Diccionario con el JSON parseado
            
        Raises:
            GeminiServiceError: Si no se puede parsear el JSON
        """
        # Intentar encontrar JSON en el texto (puede estar entre ```json o directamente)
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Buscar JSON directamente (entre llaves)
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                raise GeminiServiceError("No se encontró JSON válido en la respuesta de Gemini")
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise GeminiServiceError(f"Error al parsear JSON: {str(e)}")
    
    def generate_theory(self, tema: str) -> Dict[str, Any]:
        """
        Genera teoría educativa estructurada sobre un tema dado.
        
        Args:
            tema: El tema sobre el cual generar teoría
            
        Returns:
            Diccionario con la teoría estructurada en formato JSON
        """
        prompt = (
            f"Genera una explicación teórica completa y educativa sobre el siguiente tema: {tema}. "
            f"Debes responder ÚNICAMENTE con un objeto JSON válido (sin texto adicional, sin markdown, solo JSON) "
            f"con la siguiente estructura exacta:\n\n"
            f'{{\n'
            f'  "titulo": "Título principal del tema",\n'
            f'  "introduccion": "Una introducción clara y concisa al tema",\n'
            f'  "secciones": [\n'
            f'    {{\n'
            f'      "titulo": "Título de la sección",\n'
            f'      "contenido": "Contenido detallado de la sección"\n'
            f'    }}\n'
            f'  ],\n'
            f'  "conceptos_clave": ["concepto1", "concepto2", "concepto3"],\n'
            f'  "ejemplos": ["ejemplo1", "ejemplo2"]\n'
            f'}}\n\n'
            f"Genera entre 3 y 5 secciones. Asegúrate de que el JSON sea válido y esté bien formateado."
        )
        
        response_text = self.generate_content(prompt)
        return self._parse_json_from_text(response_text)
    
    def generate_questions_from_text(self, texto: str) -> Dict[str, Any]:
        """
        Genera preguntas educativas estructuradas basadas en un texto.
        
        Args:
            texto: El texto del cual generar preguntas
            
        Returns:
            Diccionario con las preguntas estructuradas en formato JSON
        """
        prompt = (
            f"Basándote en el siguiente contenido, genera preguntas educativas de opción múltiple (A, B, C, D) "
            f"y relevantes sobre el tema. Las preguntas deben ser claras, variadas (de comprensión, análisis, aplicación), "
            f"cortas y útiles para evaluar el aprendizaje. Genera entre 5 y 10 preguntas.\n\n"
            f"Debes responder ÚNICAMENTE con un objeto JSON válido (sin texto adicional, sin markdown, solo JSON) "
            f"con la siguiente estructura exacta:\n\n"
            f'{{\n'
            f'  "preguntas": [\n'
            f'    {{\n'
            f'      "numero": 1,\n'
            f'      "pregunta": "Texto de la pregunta",\n'
            f'      "opciones": ["Opción A", "Opción B", "Opción C", "Opción D"],\n'
            f'      "respuesta_correcta": "A",\n'
            f'      "tipo": "comprension",\n'
            f'      "dificultad": "facil"\n'
            f'    }}\n'
            f'  ]\n'
            f'}}\n\n'
            f"El tipo puede ser: 'comprension', 'analisis', o 'aplicacion'. "
            f"La dificultad puede ser: 'facil', 'media', o 'alta'. "
            f"La respuesta_correcta debe ser una de las letras: 'A', 'B', 'C', o 'D'. "
            f"Asegúrate de que el JSON sea válido y esté bien formateado.\n\n"
            f"Contenido:\n{texto}"
        )
        
        response_text = self.generate_content(prompt)
        return self._parse_json_from_text(response_text)

