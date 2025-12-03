"""
Servicio para interactuar con la API de Gemini.
Sigue el principio de Single Responsibility: solo maneja la comunicación con Gemini.
"""
import json
import re
from typing import Optional, Dict, Any, List
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
        prompt = f"""
            A partir del siguiente contenido, genera una lista de preguntas de opción múltiple en formato JSON válido siguiendo exactamente el esquema indicado más abajo."

            Contenido:
            \"\"\"{texto}\"\"\"
            

            Esquema JSON de salida:
            {{
                "questions": [
                    {{
                        "id": "integer",                // identificador único de la pregunta
                        "content": string",             // texto de la pregunta
                        "possibleAnswers": ["string"],  // lista de opciones de respuesta
                        "correctAnswer": "integer"      // índice de la respuesta correcta con respecto al arreglo "possibleAnswers"
                    }}
                ]
            }}

            Requisitos:
            - Devuelve solo el JSON válido, sin texto adicional, sin markdown, sin ```json.
            - Las preguntas deben ser claras, variadas (de comprensión, análisis, aplicación) y útiles para evaluar el aprendizaje.
            - Asegurate de que "correctAnswer" sea una de las opciones en "possibleAnswers".
            - Genera entre 5 a 10 preguntas.
            - Cada pregunta debe tener entre 3 a 5 opciones de respuesta.
            """
        
        return self.generate_content(prompt)
    
    def generate_random_topic_titles(self, cantidad: int = 3) -> Dict[str, Any]:
        """
        Genera títulos de temas educativos completamente aleatorios.
        Cada llamada genera temas diferentes gracias a la naturaleza del LLM.
        
        Args:
            cantidad: Número de títulos a generar (3-5)
            
        Returns:
            Diccionario con lista de títulos en formato JSON
        """
        prompt = f"""
            Genera {cantidad} títulos de temas educativos interesantes, variados y completamente aleatorios.
            
            IMPORTANTE: 
            - Genera títulos DIFERENTES cada vez
            - Los títulos deben ser VARIADOS y cubrir diferentes áreas del conocimiento
            - NO repitas los mismos títulos siempre
            - Títulos cortos y concisos (máximo 30 caracteres)
            - Pueden ser de cualquier área: Matemáticas, Ciencias, Historia, Arte, Tecnología, etc.
            
            Debes responder ÚNICAMENTE con un objeto JSON válido (sin texto adicional, sin markdown, solo JSON) 
            con la siguiente estructura exacta:
            
            {{
                "temas": [
                    "Título del tema 1",
                    "Título del tema 2",
                    "Título del tema 3"
                ]
            }}
            
            Requisitos:
            - Genera EXACTAMENTE {cantidad} títulos
            - Los títulos deben ser cortos, concisos y atractivos
            - VARÍA los temas - no uses siempre los mismos
            - Mezcla diferentes áreas del conocimiento
            - Asegúrate de que el JSON sea válido
            
            Ejemplos de buenos títulos:
            - "Geometría Fractal"
            - "Inteligencia Artificial"
            - "Revolución Industrial"
            - "Química Orgánica"
            - "Mitología Griega"
        """
        
        response_text = self.generate_content(prompt)
        return self._parse_json_from_text(response_text)
    
    def generate_questions_from_topic(self, tema: str, cantidad: int = 5) -> str:
        """
        Genera preguntas educativas estructuradas basadas en un tema específico.
        
        Args:
            tema: El tema sobre el cual generar preguntas
            cantidad: Cantidad de preguntas a generar (3-10)
            
        Returns:
            String con JSON de las preguntas estructuradas
        """
        prompt = f"""
            Genera {cantidad} preguntas de opción múltiple educativas sobre el siguiente tema: "{tema}"
            
            Las preguntas deben ser variadas, claras y útiles para evaluar el conocimiento sobre el tema.
            
            Debes responder ÚNICAMENTE con un objeto JSON válido (sin texto adicional, sin markdown, sin ```json) 
            siguiendo exactamente este esquema:
            
            {{
                "questions": [
                    {{
                        "id": 0,
                        "content": "Texto de la pregunta",
                        "possibleAnswers": ["opción 1", "opción 2", "opción 3", "opción 4"],
                        "correctAnswer": 1
                    }}
                ]
            }}
            
            Requisitos IMPORTANTES:
            - Genera EXACTAMENTE {cantidad} preguntas
            - El "id" debe empezar en 0 y ser secuencial (0, 1, 2, 3...)
            - "correctAnswer" debe ser el ÍNDICE (número) de la respuesta correcta en "possibleAnswers"
            - Los índices empiezan en 0 (primera opción = 0, segunda = 1, tercera = 2, etc.)
            - Cada pregunta debe tener entre 3 y 5 opciones de respuesta
            - Las preguntas deben ser variadas: comprensión, análisis y aplicación
            - Asegúrate de que el JSON sea válido
            - NO incluyas markdown, NO incluyas ```json, solo el JSON puro
        """
        
        return self.generate_content(prompt)
    
    def generate_tutor_introduction(self, tema: str) -> str:
        """
        Genera el mensaje de presentación inicial del tutor.
        
        Args:
            tema: El tema sobre el cual el tutor será experto
            
        Returns:
            Mensaje de presentación del tutor
        """
        prompt = f"""
            Eres UNIprofe, un tutor virtual experto y amigable. Te acaban de asignar ser experto en el tema: "{tema}".
            
            Tu tarea es presentarte al estudiante de manera cálida y profesional. Debes:
            
            1. Saludar con un emoji amigable (👋)
            2. Presentarte como "UNIprofe"
            3. Mencionar que eres experto en el tema específico
            4. Ofrecerte a ayudar con todas sus dudas
            5. Preguntar qué desea saber
            
            IMPORTANTE:
            - Sé amigable pero profesional
            - Usa emojis apropiados (máximo 2-3)
            - Mantén un tono entusiasta y motivador
            - El mensaje debe ser breve (2-3 oraciones)
            - NO incluyas información sobre el tema aún, solo preséntate
            
            Responde ÚNICAMENTE con el mensaje de presentación, sin texto adicional.
        """
        
        return self.generate_content(prompt)
    
    def generate_tutor_response(
        self, 
        tema: str, 
        mensaje_usuario: str, 
        historial: List[dict] = None
    ) -> str:
        """
        Genera una respuesta del tutor basada en el mensaje del usuario y el historial.
        
        Args:
            tema: El tema sobre el cual el tutor es experto
            mensaje_usuario: El mensaje/pregunta del usuario
            historial: Historial de la conversación (lista de mensajes)
            
        Returns:
            Respuesta del tutor
        """
        # Construir contexto del historial
        contexto_historial = ""
        if historial and len(historial) > 0:
            contexto_historial = "\n\nHistorial de la conversación:\n"
            for msg in historial[-10:]:  # Últimos 10 mensajes para mantener contexto
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "user":
                    contexto_historial += f"Estudiante: {content}\n"
                else:
                    contexto_historial += f"Tutor: {content}\n"
        
        prompt = f"""
            Eres UNIprofe, un tutor virtual experto y amigable especializado en: "{tema}".
            
            REGLAS IMPORTANTES:
            
            1. **Especialización**: Solo puedes responder preguntas sobre "{tema}". Si el estudiante pregunta sobre otro tema, debes amablemente recordarle que solo eres experto en "{tema}" y sugerirle que puede elegir otro tema si desea.
            
            2. **Mensajes vacíos**: Si el estudiante envía un mensaje vacío o sin contenido, responde amablemente indicando que no escribió nada y pregunta si tiene más dudas. Si no tiene más dudas, despídete cordialmente.
            
            3. **Personalidad**:
               - Sé amigable, paciente y entusiasta
               - Usa emojis apropiados (máximo 2-3 por mensaje) para hacer la conversación más agradable
               - Explica de manera clara y didáctica
               - Adapta tu lenguaje al nivel del estudiante
               - Sé alentador y positivo
            
            4. **Mantén el contexto**: Usa el historial de la conversación para dar respuestas coherentes y contextualizadas.
            
            5. **Si el estudiante se desvía del tema**: Amablemente dile algo como:
               "Hmm, esa pregunta es interesante, pero me especializo en {tema}. ¿Hay algo específico sobre {tema} que te gustaría saber? 😊"
            
            6. **Formato de respuesta**:
               - Responde directamente, sin prefijos como "Tutor:" o "UNIprofe:"
               - Mantén las respuestas concisas pero completas
               - Si es necesario, puedes hacer preguntas de seguimiento
            
            {contexto_historial}
            
            Mensaje actual del estudiante: "{mensaje_usuario}"
            
            Responde ÚNICAMENTE con tu respuesta como tutor, sin texto adicional, sin markdown, sin prefijos.
        """
        
        return self.generate_content(prompt)

