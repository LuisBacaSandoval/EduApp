"""
Configuración de la aplicación con seguridad mejorada.
Maneja todas las variables de entorno y configuraciones de forma segura.
"""
from typing import Optional
from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class Settings(BaseSettings):
    """
    Clase de configuración que centraliza todas las variables de entorno.
    Usa Pydantic Settings para validación y seguridad mejorada.
    Sigue el principio de Single Responsibility.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        # No permitir valores por defecto inseguros
        extra="ignore"
    )
    
    # API Configuration
    API_TITLE: str = "EduApp API"
    API_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # Server Configuration
    HOST: str = Field(default="0.0.0.0", description="Host del servidor")
    PORT: int = Field(default=8000, ge=1, le=65535, description="Puerto del servidor")
    
    # CORS Configuration
    CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:5173", "http://localhost:3000"],
        description="Orígenes permitidos para CORS"
    )
    
    # Gemini Configuration - USANDO SecretStr para protección
    GEMINI_API_KEY: SecretStr = Field(
        ...,
        description="API Key de Google Gemini (requerida)",
        min_length=1
    )
    GEMINI_MODEL: str = Field(
        default="gemini-2.0-flash-exp",
        description="Modelo de Gemini a utilizar"
    )
    
    # PDF Configuration
    MAX_PDF_TEXT_LENGTH: int = Field(
        default=8000,
        ge=100,
        le=100000,
        description="Longitud máxima del texto extraído de PDFs"
    )
    
    @field_validator("GEMINI_API_KEY")
    @classmethod
    def validate_api_key(cls, v: SecretStr) -> SecretStr:
        """
        Valida que la API key tenga un formato razonable.
        No expone la key completa en logs.
        """
        if not v:
            raise ValueError("GEMINI_API_KEY es requerida")
        
        # Obtener el valor para validar (sin exponerlo)
        key_value = v.get_secret_value()
        
        # Validar que no esté vacía o solo con espacios
        if not key_value or not key_value.strip():
            raise ValueError("GEMINI_API_KEY no puede estar vacía")
        
        # Validar longitud mínima razonable (las API keys suelen tener al menos 20 caracteres)
        if len(key_value.strip()) < 20:
            raise ValueError("GEMINI_API_KEY parece inválida (muy corta)")
        
        # Validar que no contenga espacios
        if " " in key_value:
            raise ValueError("GEMINI_API_KEY no debe contener espacios")
        
        return v
    
    @property
    def is_gemini_configured(self) -> bool:
        """Verifica si Gemini está configurado correctamente."""
        try:
            return bool(self.GEMINI_API_KEY and self.GEMINI_API_KEY.get_secret_value())
        except Exception:
            return False
    
    def get_gemini_api_key(self) -> str:
        """
        Método seguro para obtener la API key.
        Usa get_secret_value() para evitar exposición en logs.
        """
        return self.GEMINI_API_KEY.get_secret_value()
    
    def __repr__(self) -> str:
        """
        Representación segura que no expone la API key.
        """
        api_key_status = "configurada" if self.is_gemini_configured else "no configurada"
        return (
            f"Settings("
            f"API_TITLE={self.API_TITLE}, "
            f"GEMINI_API_KEY={api_key_status}, "
            f"GEMINI_MODEL={self.GEMINI_MODEL}, "
            f"HOST={self.HOST}, "
            f"PORT={self.PORT}"
            f")"


# Instancia global de configuración
try:
    settings = Settings()
except Exception as e:
    # En caso de error, lanzar excepción clara
    raise RuntimeError(
        f"Error al cargar configuración: {str(e)}. "
        "Por favor, verifica tu archivo .env y asegúrate de que GEMINI_API_KEY esté configurada correctamente."
    )


def validate_settings() -> None:
    """
    Valida las configuraciones al inicio de la aplicación.
    Lanza excepciones si hay problemas de configuración.
    """
    if not settings.is_gemini_configured:
        raise ValueError(
            "GEMINI_API_KEY no está configurada correctamente. "
            "Por favor, configura GEMINI_API_KEY en el archivo .env"
        )

