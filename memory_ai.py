import json
import requests

def analyze_memory(user_input):

    prompt=f"""
    Du bist ein System zur Analyse von Nutzeraussagen.

    Deine Aufgabe:
    Entscheide, ob der Nutzer:

    - eine Tatsache über sich sagt (FACT)
    - eine Erinnerung sagt (MEMORY)
    - etwas löschen will (DELETE)
    - oder nichts davon ist

    Antworte AUSSCHLIESSLICH im JSON Format.

    ---

    FACT (dauerhafte Information):
    - Name
    - Wohnort
    - Alter
    - Lieblingsspiel
    - Hobbys

    Format:
    {{
    "action": "update_fact",
    "key": "name",
    "value": "Paul"
    }}

    ---

    MEMORY (Erlebnis / Ereignis):
    {{
    "action": "save_memory",
    "content": "Ich habe heute Pizza gegessen"
    }}

    ---

    DELETE (löschen):
    {{
    "action": "delete_fact",
    "key": "name"
    }}

    ---

    NICHTS:
    {{
        "action": "nothing"
    }}

    ---

    USER:
    {user_input}
    """

    response=requests.post(
         "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    reply=response.json()["response"].strip()

    try:
        return json.loads(reply)
    
    except:
        return{"action":"nothing"}
