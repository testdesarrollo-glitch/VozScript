# Documentación API: `stt_formatter`

Bienvenido a la documentación oficial de **`stt_formatter`**. Esta librería proporciona herramientas simplificadas para capturar y transcribir audio, así como para procesar y estructurar texto utilizando modelos de inteligencia artificial locales a través de **Ollama**.

---

## Instalación

### Instalación Local (Modo Desarrollo)
Para instalar la librería en tu entorno local y que los cambios en el código se reflejen en tiempo real:
```bash
pip install -e .
```

### Instalación desde otro Repositorio (Vía Git)
Si el proyecto se encuentra alojado en un repositorio (GitHub, GitLab, etc.), puedes instalarlo directamente con:
```bash
pip install git+https://github.com/testdesarrollo-glitch/VozScript
```

---

## Configuración del Entorno

Asegúrate de tener **Ollama** en ejecución en tu máquina o contenedor antes de usar el módulo de formateo (`formatter.py`).
Puedes definir la variable de entorno `OLLAMA_HOST` si tu servidor corre en un puerto o máquina diferente.
*   **Por defecto:** `http://localhost:11434`

---

## Referencia de Módulos y Funciones

### 1. Módulo de Audio (`audio_capture.py`)

Este módulo se encarga del procesamiento y la transcripción de archivos de audio empleando `SpeechRecognition`.

#### `transcribe_audio(route_audio, language="es-ES")`
Transcribe un archivo de audio a texto utilizando Google Speech Recognition.

*   **Parámetros:**
    *   `route_audio` *(str)*: La ruta absoluta o relativa al archivo de audio (ej. `.wav`, `.flac`).
    *   `language` *(str, opcional)*: El código de idioma para la transcripción. Por defecto es `"es-ES"` (Español).
*   **Retorna:**
    *   *(str)*: El texto transcrito del archivo de audio. Si ocurre un error durante el procesamiento o el audio es ininteligible, retorna una cadena de texto detallando el error específico.

**Ejemplo de uso:**
```python
from stt_formatter.audio_capture import transcribe_audio

texto = transcribe_audio("assets/Grabacion_2.wav")
print(texto)
```

---

### 2. Módulo de Formateo e IA (`formatter.py`)

Este módulo conecta tu código con modelos locales de LLM (Large Language Models) para realizar procesamiento de lenguaje natural avanzado.

#### `sumarize_corpus(corpus, model="llama3")`
Genera un resumen claro y conciso del texto proporcionado utilizando un LLM local.

*   **Parámetros:**
    *   `corpus` *(str)*: El bloque extenso de texto en bruto que necesita ser resumido.
    *   `model` *(str, opcional)*: El nombre del modelo de Ollama a utilizar para la inferencia. Por defecto es `"llama3"`.
*   **Retorna:**
    *   *(str)*: La versión resumida del texto generada por el modelo.

**Ejemplo de uso:**
```python
from stt_formatter.formatter import sumarize_corpus

resumen = sumarize_corpus("Texto muy largo transcrito previamente...", model="llama3")
print(resumen)
```

#### `generate_json_from_corpus(corpus, requirements, model="llama3")`
Extrae información de un corpus de texto y la estructura en un objeto JSON basándose en requisitos de esquema específicos.

*   **Parámetros:**
    *   `corpus` *(str)*: El texto en bruto del cual se extraerá la información.
    *   `requirements` *(dict)*: Un diccionario que define las claves JSON deseadas y sus tipos de datos esperados.
    *   `model` *(str, opcional)*: El nombre del modelo de Ollama a utilizar. Por defecto es `"llama3"`.
*   **Retorna:**
    *   *(dict)*: Un diccionario parseado que contiene los datos extraídos. Si el LLM falla al generar un JSON válido, retorna un diccionario con la clave `"error"` y la respuesta en bruto.

**Ejemplo de uso:**
```python
from stt_formatter.formatter import generate_json_from_corpus

# 1. Definimos la estructura que necesitamos
esquema = {
    "nombre_paciente": "string",
    "sintomas": "array",
    "edad": "integer"
}

# 2. Ejecutamos la extracción
datos = generate_json_from_corpus(
    corpus="El paciente Juan Pérez, de 45 años, presenta fiebre y dolor de cabeza.", 
    requirements=esquema
)

print(datos['nombre_paciente']) # Salida: "Juan Pérez"
```