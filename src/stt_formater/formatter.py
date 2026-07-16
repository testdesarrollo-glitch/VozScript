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

def generate_json_from_corpus(corpus: str, requirements: dict, model: str = "llama3") -> str:
    """
    Generate json from corpus
    args:
        corpus: str
        requirements: dict
        model: str
    return:
        json: str
    """

    req_str = json.dumps(requirements, ensure_ascii=False, indent=2)

    prompt = f"""
    Basado en el siguiente texto:
    {corpus}
    
    Genera un objeto JSON que cumpla estrictamente con la siguiente estructura y requerimientos:
    {req_str}
    
    Responde ÚNICAMENTE con el JSON.
    """

    response = ollama.chat(
        model=model,
        messages=[{'role': 'user', 'content': prompt}],
        format='json'
    )

    try:
        return json.loads(response['message']['content'])
    except json.JSONDecodeError:
        return {"error": "El modelo no generó un JSON válido", "raw_response": response['message']['content']}