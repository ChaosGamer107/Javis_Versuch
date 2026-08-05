import requests
import json
from config import MODEL, OLLAMA_URL

def analyze_conversation(user_input):

    prompt=f"""
Du bist der Gesprächsanalysator von Nova.

Analysiere die Nachricht des Nutzer.

Antworte ausschließlich als JSON.
Kein zusätlicher Text.

Schema:

{{
    "type":"",
    "topic":"", 
    "goal":"",
    "emotion":"",
    "should_ask_question":false,
    "should_encourage":false,
    "should_use_memory":false,
    "should_joke":false,
    "answer_length":""
}}

Mögliche type:

chat
coding
question
learning
personal
command

Mögliche topic:

smalltalk
programmierung
nova
schule
bewerbung
minecraft
gaming
technik
ki
musik
filme
sport
persönlich
allgemein

Mögliche emotion:

neutral
happy
sad
angry
frustrated
excited

Mögliche answer_length:

short
medium
long

Regeln:

- Bestimme das Hauptthema der Nachricht.
- Bestimme das eigentliche Ziel des Nutzers.
- Erkenne die Stimmung des Nutzers.
- should_ask_question ist true, wenn eine Rückfrage das Gespräch sinnvoll weiterführen würde.
- should_encourage ist true, wenn der Nutzer Ermutigung oder Motivation gebrauchen kann.
- should_use_memory ist true, wenn vorhandene Informationen über den Nutzer relevant sein könnten.
- should_joke ist true, wenn ein lockerer oder humorvoller Ton passend wäre.
- answer_length beschreibt, wie ausführlich Nova antworten sollte.
- Bei normalem Smalltalk soll die Antwort kurz oder mittel sein.
- Bei technischen Fragen darf die Antwort länger sein.

Nachricht des Nutzers:

{user_input}
"""

    response=requests.post(
        OLLAMA_URL,
        json={
            "model":MODEL,
            "prompt":prompt,
            "stream":False
        }
    )    

    reply=response.json()["response"]

    try:
        start=reply.find("{")
        end=reply.find("}")+1

        if start== -1 or end == 0:
            raise ValueError("Kein JSON gefunden")

        return json.loads(reply[start:end])

    except Exception:

        return{
            "type":"chat",
            "topic":"allgemein",
            "goal":"",
            "emotion":"neutral",
            "should_ask_question":False,
            "should_encourage":False,
            "should_use_memory":False,
            "should_joke":False,
            "answer_length":"medium"
        }