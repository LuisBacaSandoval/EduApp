# EduApp API - Backend

API REST desarrollada con FastAPI para la generación de contenido educativo utilizando Google Gemini como modelo de lenguaje (LLM). Esta API proporciona endpoints para generar teoría educativa sobre temas específicos y generar preguntas basadas en el contenido de documentos PDF.

## Tabla de Contenidos

- [Descripción](#descripción)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Arquitectura y Flujo](#arquitectura-y-flujo)
- [Endpoints](#endpoints)
- [Seguridad](#seguridad)
- [Testing](#testing)
- [Solución de Problemas](#solución-de-problemas)

---

## Descripción

EduApp API es el backend de una aplicación educativa que permite:

- **Generar teoría educativa**: A partir de un tema de texto, genera explicaciones teóricas completas y didácticas usando Google Gemini.
- **Generar preguntas desde PDFs**: Procesa documentos PDF, extrae su contenido y genera preguntas educativas relevantes sobre el material.

La aplicación está construida siguiendo principios SOLID y buenas prácticas de desarrollo, con una arquitectura escalable y mantenible.

---

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.10 o superior**
- **pip** (gestor de paquetes de Python)
- **API Key de Google Gemini** ([Obtener aquí](https://aistudio.google.com/app/apikey))

### Verificar Python

```bash
python3 --version
# Debe mostrar Python 3.10.x o superior
```

---

## Instalación

### Paso 1: Clonar el Repositorio

```bash
cd /ruta/al/proyecto/EduApp/server
```

### Paso 2: Crear Entorno Virtual

Es altamente recomendable usar un entorno virtual para aislar las dependencias del proyecto.

#### Opción A: Usando `venv` (Recomendado)

```bash
# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno virtual
# En Linux/Mac:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

#### Opción B: Usando `virtualenv`

```bash
# Instalar virtualenv si no lo tienes
pip install virtualenv

# Crear el entorno virtual
virtualenv venv

# Activar el entorno virtual
# En Linux/Mac:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

**Nota**: Cuando el entorno virtual está activado, verás `(venv)` al inicio de tu línea de comandos.

### Paso 3: Instalar Dependencias

```bash
# Asegúrate de que el entorno virtual esté activado
pip install --upgrade pip
pip install -r requirements.txt
```

Las dependencias instaladas incluyen:
- `fastapi`: Framework web para construir la API
- `uvicorn`: Servidor ASGI para ejecutar FastAPI
- `google-genai`: Cliente oficial de Google Gemini
- `pydantic-settings`: Gestión segura de configuración
- `pypdf2`: Procesamiento de archivos PDF
- `python-dotenv`: Carga de variables de entorno

---

## Configuración

### Paso 1: Crear Archivo de Configuración

Crea un archivo `.env` en la raíz del directorio `server/`:

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar el archivo .env
nano .env
# O usar tu editor preferido
```

### Paso 2: Configurar Variables de Entorno

Edita el archivo `.env` con tus valores:

```env
# API Key de Google Gemini (REQUERIDA)
# Obtén tu API key en: https://aistudio.google.com/app/apikey
# La API key debe tener al menos 20 caracteres y no contener espacios
# IMPORTANTE: Si recibes error 403 PERMISSION_DENIED, ve a Google Cloud Console
# y elimina las restricciones de "Referer HTTP" de tu API key
GEMINI_API_KEY=tu_api_key_aqui_minimo_20_caracteres

# Modelo de Gemini a utilizar
GEMINI_MODEL=gemini-2.0-flash-exp

# Configuración del servidor
HOST=0.0.0.0
PORT=8000

# Configuración de PDF
# Longitud máxima del texto extraído de PDFs (100-100000)
MAX_PDF_TEXT_LENGTH=8000
```

**IMPORTANTE DE SEGURIDAD:**
- **NUNCA** subas el archivo `.env` al repositorio
- **NUNCA** compartas tu API key
- El archivo `.env` está en `.gitignore` para protección automática

### Paso 3: Verificar Configuración

```bash
# Verificar que el archivo .env existe
ls -la .env

# Verificar que está en .gitignore
git check-ignore .env
# Debe retornar: .env
```

---

## Estructura del Proyecto

```
server/
├── app/                          # Módulo principal de la aplicación
│   ├── __init__.py
│   ├── api/                      # Capa de API
│   │   ├── __init__.py
│   │   └── routes/               # Rutas de la API
│   │       ├── __init__.py       # Router principal
│   │       ├── teoria.py         # Endpoints de teoría
│   │       └── pdf.py            # Endpoints de PDF
│   ├── core/                     # Núcleo de la aplicación
│   │   ├── __init__.py
│   │   ├── config.py            # Configuración centralizada
│   │   ├── dependencies.py      # Inyección de dependencias
│   │   └── exceptions.py        # Excepciones personalizadas
│   ├── models/                   # Modelos de datos
│   │   ├── __init__.py
│   │   └── schemas.py           # Schemas Pydantic (validación)
│   ├── services/                 # Servicios de negocio
│   │   ├── __init__.py
│   │   ├── gemini_service.py    # Servicio de Gemini
│   │   └── pdf_service.py        # Servicio de PDF
│   └── main.py                  # Configuración de FastAPI
├── main.py                       # Punto de entrada del servidor
├── requirements.txt              # Dependencias del proyecto
├── .env.example                  # Plantilla de configuración
├── .gitignore                    # Archivos ignorados por Git
└── README.md                     # Este archivo
```

### Descripción de Componentes

#### `app/core/`
- **`config.py`**: Centraliza todas las configuraciones y variables de entorno. Usa `pydantic-settings` para validación y seguridad.
- **`dependencies.py`**: Implementa inyección de dependencias. Proporciona funciones factory para crear servicios.
- **`exceptions.py`**: Define excepciones personalizadas para manejo de errores específicos.

#### `app/services/`
- **`gemini_service.py`**: Abstrae la comunicación con la API de Google Gemini. Maneja la generación de contenido.
- **`pdf_service.py`**: Procesa archivos PDF y extrae texto. Valida tipos de archivo y maneja errores.

#### `app/api/routes/`
- **`teoria.py`**: Define endpoints para generación de teoría educativa.
- **`pdf.py`**: Define endpoints para procesamiento de PDFs y generación de preguntas.

#### `app/models/`
- **`schemas.py`**: Define modelos Pydantic para validación de requests y responses.

---

## Arquitectura y Flujo

### Principios SOLID Aplicados

La aplicación sigue una arquitectura basada en principios SOLID:

- **Single Responsibility**: Cada módulo tiene una única responsabilidad
- **Open/Closed**: Fácil de extender sin modificar código existente
- **Liskov Substitution**: Servicios pueden ser intercambiables
- **Interface Segregation**: Interfaces específicas y claras
- **Dependency Inversion**: Dependencias inyectadas, no hardcodeadas

### Flujo de Configuración

```
┌─────────────────┐
│   archivo .env  │  ← Variables de entorno
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│  app/core/config.py            │
│  - Carga automática del .env   │
│  - Settings (BaseSettings)     │
│  - Validación y centralización │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  app/core/dependencies.py        │
│  - Inyección de dependencias   │
│  - get_gemini_service()        │
│  - get_pdf_service()           │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Servicios y Rutas              │
│  - Reciben valores inyectados   │
│  - NO tienen valores hardcoded  │
└─────────────────────────────────┘
```

### Flujo de una Petición

#### Ejemplo: Generar Teoría

```
1. Cliente → POST /api/teoria/generar
   ↓
2. app/api/routes/teoria.py
   - Valida request con TheoryRequest (Pydantic)
   - Obtiene GeminiService inyectado
   ↓
3. app/services/gemini_service.py
   - Genera prompt educativo
   - Llama a API de Gemini
   ↓
4. Google Gemini API
   - Procesa prompt
   - Genera teoría
   ↓
5. Response → Cliente
   - TheoryResponse con teoría generada
```

#### Ejemplo: Generar Preguntas desde PDF

```
1. Cliente → POST /api/pdf/generar-preguntas
   ↓
2. app/api/routes/pdf.py
   - Valida que el archivo sea PDF
   - Obtiene servicios inyectados
   ↓
3. app/services/pdf_service.py
   - Extrae texto del PDF
   - Limita longitud según configuración
   ↓
4. app/services/gemini_service.py
   - Genera prompt con texto extraído
   - Llama a API de Gemini
   ↓
5. Google Gemini API
   - Procesa contenido
   - Genera preguntas educativas
   ↓
6. Response → Cliente
   - PDFQuestionsResponse con preguntas
```

---

## Endpoints

### Base

#### `GET /`
Información básica de la API.

**Response:**
```json
{
  "message": "EduApp API está funcionando"
}
```

#### `GET /health`
Estado de salud de la API.

**Response:**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "gemini_configured": true
}
```

---

### Teoría

#### `POST /api/teoria/generar`
Genera teoría educativa sobre un tema dado.

**Request Body:**
```json
{
  "tema": "La fotosíntesis en las plantas"
}
```

**Response:**
```json
{
  "tema": "La fotosíntesis en las plantas",
  "teoria": "La fotosíntesis es un proceso biológico mediante el cual las plantas...",
  "success": true
}
```

**Códigos de Estado:**
- `200`: Éxito
- `400`: Error de validación
- `500`: Error del servidor o API key no configurada

---

### PDF

#### `POST /api/pdf/generar-preguntas`
Genera preguntas educativas basadas en el contenido de un PDF.

**Request:**
- **Content-Type**: `multipart/form-data`
- **Body**: Archivo PDF en el campo `file`

**Response:**
```json
{
  "nombre_archivo": "documento.pdf",
  "preguntas": "1. ¿Cuál es el tema principal del documento?\n2. ¿Qué conceptos clave se mencionan?...",
  "success": true
}
```

**Códigos de Estado:**
- `200`: Éxito
- `400`: Error de validación (archivo no es PDF o no tiene texto)
- `500`: Error del servidor o API key no configurada

**Limitaciones:**
- El texto extraído se limita a `MAX_PDF_TEXT_LENGTH` caracteres (por defecto 8000)
- Solo se aceptan archivos con `content-type: application/pdf`

---

## Seguridad

### Medidas Implementadas

1. **SecretStr de Pydantic**: Las API keys se almacenan usando `SecretStr`, que previene exposición accidental en logs.

2. **Validación de API Keys**: 
   - Validación de formato al inicio
   - Verificación de longitud mínima (20 caracteres)
   - Rechazo de keys con espacios

3. **Variables de Entorno**: 
   - Las API keys **NUNCA** se hardcodean en el código
   - Se cargan desde archivos `.env` protegidos por `.gitignore`

4. **Manejo Seguro de Errores**: 
   - Los errores no exponen información sensible
   - Los mensajes de error no incluyen la API key

### Checklist de Seguridad

- El archivo `.env` está en `.gitignore`
- No se hacen commits del archivo `.env`
- Se usa `.env.example` como plantilla
- La API key no se expone en logs o representaciones
- Validación automática al inicio de la aplicación

### Qué NO Hacer

- **NUNCA** hagas commit del archivo `.env`  
- **NUNCA** hardcodees la API key en el código  
- **NUNCA** compartas la API key por email, Slack, o mensajes  
- **NUNCA** imprimas la API key en logs o console  
- **NUNCA** uses la misma API key en desarrollo y producción  
- **NUNCA** expongas la API key en el frontend  

---

## Testing

### Documentación Interactiva

La API incluye documentación interactiva generada automáticamente:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Ejemplos con cURL

#### Generar Teoría

```bash
curl -X POST "http://localhost:8000/api/teoria/generar" \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "La fotosíntesis"
  }'
```

#### Generar Preguntas desde PDF

```bash
# Forma básica
curl -X POST "http://localhost:8000/api/pdf/generar-preguntas" \
  -F "file=@ruta/al/documento.pdf"

# Con más detalles (verbose) para ver la respuesta completa
curl -X POST "http://localhost:8000/api/pdf/generar-preguntas" \
  -F "file=@ruta/al/documento.pdf" \
  -v

# Ejemplo con ruta absoluta
curl -X POST "http://localhost:8000/api/pdf/generar-preguntas" \
  -F "file=@/home/usuario/documentos/mi_documento.pdf"

# Ejemplo con ruta relativa (desde el directorio actual)
curl -X POST "http://localhost:8000/api/pdf/generar-preguntas" \
  -F "file=@./documento.pdf"
```

### Ejemplos con Python

```python
import requests

# Generar teoría
response = requests.post(
    "http://localhost:8000/api/teoria/generar",
    json={"tema": "La fotosíntesis"}
)
print(response.json())

# Generar preguntas desde PDF
with open("documento.pdf", "rb") as f:
    files = {"file": f}
    response = requests.post(
        "http://localhost:8000/api/pdf/generar-preguntas",
        files=files
    )
    print(response.json())
```

---

## Ejecutar el Servidor

### Modo Desarrollo

```bash
# Asegúrate de que el entorno virtual esté activado
python main.py
```

El servidor se ejecutará en `http://localhost:8000` con recarga automática habilitada.

### Modo Producción

```bash
# Usando uvicorn directamente
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Con múltiples workers (recomendado para producción)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Solución de Problemas

### Error: "403 PERMISSION_DENIED - API_KEY_HTTP_REFERRER_BLOCKED"

**Problema**: La API key de Gemini tiene restricciones de referer HTTP configuradas que bloquean solicitudes desde servidores backend.

**Solución**:

1. Ve a [Google Cloud Console - API Keys](https://console.cloud.google.com/apis/credentials)
2. Busca y selecciona tu API key de Gemini
3. En la sección "Restricciones de aplicación", busca "Restricciones de referer HTTP"
4. Tienes dos opciones:

   **Opción A (Recomendada para desarrollo):**
   - Selecciona "Ninguna" en las restricciones de referer HTTP
   - Esto permite solicitudes desde cualquier origen (solo para desarrollo)

   **Opción B (Para producción):**
   - Si necesitas mantener restricciones, elimina las restricciones de referer HTTP
   - En su lugar, usa restricciones de IP o de aplicación para mayor seguridad
   - Para servidores backend, las restricciones de referer HTTP no funcionan porque no hay referer

5. Guarda los cambios
6. Espera unos minutos para que los cambios se propaguen
7. Prueba nuevamente tu solicitud

**Nota**: Las restricciones de referer HTTP están diseñadas para aplicaciones web frontend. Para APIs backend, debes usar otras formas de restricción como IP o no usar restricciones y confiar en mantener la API key secreta.

### Error: "GEMINI_API_KEY es requerida"

**Problema**: La API key no está configurada o es inválida.

**Solución**:
1. Verifica que el archivo `.env` existe en `server/`
2. Verifica que `GEMINI_API_KEY` está configurada en `.env`
3. Verifica que la API key tiene al menos 20 caracteres
4. Verifica que no hay espacios en la API key
5. Reinicia el servidor después de cambiar `.env`

### Error: "No se pudo extraer texto del PDF"

**Problema**: El PDF no contiene texto extraíble o está escaneado (imagen).

**Solución**:
- Asegúrate de que el PDF contiene texto (no es solo una imagen escaneada)
- Si el PDF es escaneado, usa OCR antes de procesarlo

### Error: "El archivo debe ser un PDF"

**Problema**: El archivo subido no es un PDF válido.

**Solución**:
- Verifica que el archivo tiene extensión `.pdf`
- Verifica que el `content-type` es `application/pdf`

### Error de Conexión con Gemini

**Problema**: No se puede conectar a la API de Gemini.

**Solución**:
1. Verifica tu conexión a internet
2. Verifica que la API key es válida
3. Verifica que tienes créditos/quota en tu cuenta de Google Cloud
4. Revisa los logs del servidor para más detalles

### El Servidor No Inicia

**Problema**: Error al iniciar el servidor.

**Solución**:
1. Verifica que Python 3.10+ está instalado
2. Verifica que el entorno virtual está activado
3. Verifica que todas las dependencias están instaladas: `pip install -r requirements.txt`
4. Verifica que el archivo `.env` está configurado correctamente
5. Revisa los mensajes de error para más detalles

---

## Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido para construir APIs
- **Uvicorn**: Servidor ASGI de alto rendimiento
- **Google Gemini**: Modelo de lenguaje para generación de contenido
- **Pydantic**: Validación de datos y configuración
- **PyPDF2**: Procesamiento de archivos PDF
- **Python-dotenv**: Gestión de variables de entorno

---

## Notas Adicionales

- La configuración se centraliza en `app/core/config.py`
- Las dependencias se inyectan mediante FastAPI `Depends()`
- Todas las variables de entorno se cargan desde `.env`
- El código sigue principios SOLID para mantenibilidad
- La aplicación está lista para escalar y agregar nuevas funcionalidades

---

## Licencia

Este proyecto es parte de EduApp, una aplicación educativa desarrollada para el curso de Interacción Humano-Computadora.

---

## Contacto y Soporte

Para dudas o problemas, contacta al equipo de desarrollo.

---

**Última actualización**: Noviembre 2024
