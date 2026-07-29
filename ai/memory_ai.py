import json
import requests
from config import MODEL, OLLAMA_URL

def analyze_memory(user_input):

    prompt=f"""
Du bist das Langzeitgedächtnis von Nova.

Deine Aufgabe ist zu entscheiden, ob die Nachricht dauerhaft gespeichert werden soll.

Antworte ausschließlich als JSON.

Mögliche Aktionen:

1.

{{
    "action":"update_fact",
    "key":"",
    "value":""
}}

2.

{{
    "action":"save_memory",
    "content":""
}}

3.

{{
    "action":"delete_fact",
    "key":""
}}

4.

{{
    "action":"none"
}}

Ein FACT ist dauerhaft gültig.

Beispiele:

- Name
- Alter
- Wohnort
- Lieblingsspiel
- Lieblingsfarbe
- Beruf
- Schule
- Ausbildung
- Hobbys
- Haustiere
- Lieblingsmusik

Eine MEMORY ist ein Erlebnis oder Ereignis.

Beispiele:

- Heute war ich im Kino.
- Ich habe Nova weiterentwickelt.
- Ich habe eine Klausur geschrieben.
- Ich war heute krank.

Wenn nichts gespeichert werden soll:

{{"action":"none"}}

Nachricht:

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

    reply=response.json()["response"].strip()

    try:

        start=reply.find("{")
        end=reply.find("}")+1

        return json.loads(reply[start:end])

    except:

        return {
            "action":"none"
        }