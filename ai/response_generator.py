import requests
from config import MODEL, OLLAMA_URL

def improve_response(user_input, reply):

    prompt=f"""
Du bist Nova.

Verbessere dein Antwort.

Regeln:

-Keine Floskeln.
-Keine Wiederholung.
-Antworte natürlich.
-Antworte nicht wie ChatGPT.
-Antwort nicht wie Wikipedia.
-Falls sinvoll, stelle genau eine Rückfrage.
-Nutze bekannte Information über den Nutzen.

Nachricht des Nutzer:
{user_input}

Deiner erste Antwort:
{reply}

Verbesserte Antwort:
"""

    response=requests.post(
        OLLAMA_URL,
        json={
            "model":MODEL,
            "prompt":prompt,
            "stream":False
        }
    )

    return response.json()["response"].strip()