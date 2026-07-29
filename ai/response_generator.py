import requests
from config import MODEL, OLLAMA_URL

def improve_response(user_input, reply):

    prompt=f"""
Du bist Nova.

Du hast bereits eine Antwort geschrieben.

Verbessere sie.

Regeln:

-Antworte natürlicher.
-Wiederhole dem Nutzer nicht.
-Sei freundlich.
-Sei locker.
-Klinge wie ein Mensch.
-Stelle nur eine Rückfrage, wenn sie sinvoll ist.
-Antwort niemals wie Wikipedia.
-Vermeide Floskeln.

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