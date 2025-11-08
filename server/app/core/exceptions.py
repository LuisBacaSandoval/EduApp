"""
Excepciones personalizadas de la aplicación.
Permite manejo de errores más específico y claro.
"""


class EduAppException(Exception):
    """Excepción base de la aplicación."""
    pass


class GeminiServiceError(EduAppException):
    """Excepción relacionada con el servicio de Gemini."""
    pass


class PDFServiceError(EduAppException):
    """Excepción relacionada con el servicio de PDF."""
    pass


class ValidationError(EduAppException):
    """Excepción relacionada con validación de datos."""
    pass

