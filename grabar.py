import pyaudio
import wave

def grabar_microfono(duracion_segundos=5, nombre_archivo="src/examples/audio_test.wav"):
    FORMATO = pyaudio.paInt16
    CANALES = 1
    TASA_MUESTREO = 16000  # 16kHz es ideal para SpeechRecognition
    TAMANO_CHUNK = 1024

    audio = pyaudio.PyAudio()

    print(f"🎙️ Grabando por {duracion_segundos} segundos... ¡Habla ahora!")
    
    stream = audio.open(format=FORMATO, channels=CANALES,
                        rate=TASA_MUESTREO, input=True,
                        frames_per_buffer=TAMANO_CHUNK)
    
    frames = []

    for _ in range(0, int(TASA_MUESTREO / TAMANO_CHUNK * duracion_segundos)):
        data = stream.read(TAMANO_CHUNK)
        frames.append(data)

    print("🛑 Grabación finalizada.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Guardar en la carpeta compartida con Docker
    wf = wave.open(nombre_archivo, 'wb')
    wf.setnchannels(CANALES)
    wf.setsampwidth(audio.get_sample_size(FORMATO))
    wf.setframerate(TASA_MUESTREO)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"💾 Archivo guardado en: {nombre_archivo}")

if __name__ == "__main__":
    grabar_microfono(duracion_segundos=7)