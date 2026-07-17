import speech_recognition as sr

def transcribe_audio(route_audio: str, language: str = "es-ES") -> str:
    """
    Transcribe audio to text
    args:
        route_audio: str
        language: str
    return:
        transcription: str
    """

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(route_audio) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.record(source)
        
        text = recognizer.recognize_google(audio_data, language=language)
        return text

    except sr.UnknownValueError as e:
        print("No se pudo transcribir el audio")
        return f"{e}"
    except sr.RequestError as e:
        print(f"Error al realizar la solicitud")
        return f"{e}"