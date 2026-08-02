import requests
from config import MODEL, OLLAMA_URL

def ask_llama(prompt):

    response=requests.post(
        OLLAMA_URL,
        json={
            "model":MODEL,
            "prompt":prompt,
            "stream":False
        }
    )

    return response.json()["response"].strip()

