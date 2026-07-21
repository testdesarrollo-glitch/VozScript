import ollama
import json
import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
client = ollama.Client(host=OLLAMA_HOST)


def sumarize_corpus(corpus: str, model: str = "llama3") -> str:
    """
    Sumarize corpus
    args:
        corpus: str
        model: str
    return:
        summary: str
    """
    prompt = f"Actúa como un asistente experto. Resume el siguiente texto de manera clara y concisa:\n\n{corpus}"

    response = client.chat(model=model, messages=[
        {'role': 'user', 'content': prompt}
    ])
    return response['message']['content']


def generate_json_from_corpus(corpus: str, requirements: dict, model: str = "llama3") -> dict:
    """
    Generate json from corpus, forzando el esquema exacto de campos mediante
    JSON Schema (structured outputs de Ollama), en vez de format='json' libre.
    args:
        corpus: str
        requirements: dict
        model: str
    return:
        json: dict
    """
    req_str = json.dumps(requirements, ensure_ascii=False, indent=2)

    # Esquema JSON real: fuerza claves EXACTAS y planas (sin anidar sub-objetos)
    schema = {
        "type": "object",
        "properties": {
            field_name: {"type": "string"} for field_name in requirements.keys()
        },
        "required": list(requirements.keys())
    }

    prompt = f"""
    Basado en el siguiente texto transcrito:
    {corpus}

    Extrae la información y complétala en los siguientes campos:
    {req_str}

    Reglas estrictas:
    - Usa EXACTAMENTE los nombres de clave indicados arriba, sin anidar en sub-objetos.
    - No agregues, renombres, ni traduzcas los nombres de clave.
    - Si no encuentras información para un campo, usa una cadena vacía "".
    """

    response = client.chat(
        model=model,
        messages=[{'role': 'user', 'content': prompt}],
        format=schema,
        options={'temperature': 0}
    )
    try:
        return json.loads(response['message']['content'])
    except json.JSONDecodeError:
        return {"error": "El modelo no generó un JSON válido", "raw_response": response['message']['content']}