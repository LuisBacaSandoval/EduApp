"""
Servicio para procesar archivos PDF.
Sigue el principio de Single Responsibility: solo maneja la extracción de texto de PDFs.
"""
import io
from typing import Optional
from PyPDF2 import PdfReader
from app.core.exceptions import PDFServiceError


class PDFService:
    """
    Servicio para extraer texto de archivos PDF.
    Abstrae la lógica de procesamiento de PDFs.
    """
    
    def __init__(self, max_text_length: int):
        """
        Inicializa el servicio de PDF.
        
        Args:
            max_text_length: Longitud máxima del texto extraído (obtenida de settings)
        """
        self.max_text_length = max_text_length
    
    def extract_text(self, pdf_content: bytes) -> str:
        """
        Extrae texto de un archivo PDF.
        
        Args:
            pdf_content: Contenido del PDF en bytes
            
        Returns:
            El texto extraído del PDF
            
        Raises:
            PDFServiceError: Si hay un error al procesar el PDF
        """
        try:
            pdf_reader = PdfReader(io.BytesIO(pdf_content))
            texto_pdf = ""
            
            # Extraer texto de todas las páginas
            for page in pdf_reader.pages:
                texto_pdf += page.extract_text() + "\n"
            
            texto_pdf = texto_pdf.strip()
            
            if not texto_pdf:
                raise PDFServiceError(
                    "No se pudo extraer texto del PDF. "
                    "Asegúrate de que el PDF contenga texto."
                )
            
            # Limitar la longitud del texto si es necesario
            if len(texto_pdf) > self.max_text_length:
                texto_pdf = texto_pdf[:self.max_text_length]
            
            return texto_pdf
        
        except PDFServiceError:
            raise
        except Exception as e:
            raise PDFServiceError(f"Error al procesar el PDF: {str(e)}")
    
    def validate_pdf_content_type(self, content_type: Optional[str]) -> bool:
        """
        Valida que el tipo de contenido sea un PDF.
        
        Args:
            content_type: El tipo de contenido del archivo
            
        Returns:
            True si es un PDF, False en caso contrario
        """
        return content_type == "application/pdf"

