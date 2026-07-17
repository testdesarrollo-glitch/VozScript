import os
import sys
import json

# Asegurar que Python pueda encontrar el módulo src si se ejecuta desde diferentes carpetas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Importar las funciones que creaste en tu librería
from src.stt_formatter.audio_capture import transcribe_audio
from src.stt_formatter.formatter import sumarize_corpus, generate_json_from_corpus

def ejecutar_demo():
    print("=" * 60)
    print(" INICIANDO DEMO DE PROCESAMIENTO DE AUDIO Y LLM ")
    print("=" * 60)

    # 1. Definir rutas (Se recomienda usar un archivo .wav de prueba dentro del proyecto)
    # Reemplaza 'audio_test.wav' con el nombre real de tu archivo de pruebas
    ruta_audio = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Grabación-_2_.wav'))
    
    if not os.path.exists(ruta_audio):
        print(f"\n[⚠️ Alerta]: No se encontró el archivo de prueba en: {ruta_audio}")
        print("Por favor, coloca un archivo válido '.wav' en esa ruta para completar la prueba.")
        return

    # 2. Paso 1: Transcripción del audio (Speech to Text)
    print("\n[Paso 1] Transcribiendo el archivo de audio...")
    corpus_transcrito = transcribe_audio(ruta_audio, language="es-ES")
    
    print("\n--- Texto Transcrito Obtenido ---")
    print(corpus_transcrito)
    print("---------------------------------")

    # Validar si hubo un error en la transcripción antes de continuar
    if "Error" in corpus_transcrito or "no pudo ser entendido" in corpus_transcrito:
        print("[❌ Error]: Deteniendo el flujo debido a fallas en la transcripción.")
        return

    # 3. Paso 2: Generar Resumen con Ollama
    print("\n[Paso 2] Enviando corpus a Ollama para generar resumen...")
    resumen = sumarize_corpus(corpus_transcrito, model="llama3")
    
    print("\n--- Resumen del Texto ---")
    print(resumen)
    print("-------------------------")

    # 4. Paso 3: Extraer requerimientos y estructurar a JSON
    print("\n[Paso 3] Estructurando el corpus en el esquema JSON solicitado...")
    
    # Aquí defines libremente qué campos e instrucciones quieres que el LLM extraiga del audio
    requerimientos_json = {
        "tema_principal": "El asunto central o tópico del que trata el audio",
        "puntos_clave": ["Lista de las 3 ideas o acuerdos más importantes mencionados"],
        "compromisos": [
            {
                "responsable": "Nombre de la persona encargada (si se menciona, si no 'No especificado')",
                "tarea": "Descripción de la acción que debe realizar"
            }
        ],
        "sentimiento_general": "Clasificar entre: Positivo, Neutro o Negativo"
    }

    resultado_json = generate_json_from_corpus(
        corpus=corpus_transcrito, 
        requirements=requerimientos_json, 
        model="llama3"
    )
    
    print("\n--- JSON Estructurado Final ---")
    print(json.dumps(resultado_json, indent=4, ensure_ascii=False))
    print("--------------------------------")
    
    print("\n🎉 ¡Procesamiento completado con éxito!")

if __name__ == "__main__":
    ejecutar_demo()