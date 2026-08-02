import json
import requests
from config import MODEL, OLLAMA_URL

def create_plan(user_input):

    prompt="""
Du bist der interne Planer von Nova.

Analysiere die Nachricht.

Antworte ausschließlich als JSON.

Schema:

{{
    "goal":"",
    "conversation_type":"",
    "use_memory":true,
    "use_tools":false,
    "tool":"",
    "continue_topic":true,
    "ask_followup":false
}}

Regeln:

-use_memory = Soll Nova Erinnerungen benutzen ?
-use_tools = Muss ein Tool genutzt werden ?
-tool = Name des Tools oder Leer
-continue_topic = Soll das aktuell Thema fortgesetzt werden ?
-ask_followup = Soll Nova eine Rückfrage stellen ?

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

    reply=response.json()["response"]

    try:
        start=reply.find("{")
        end=reply.find("}")+1

        return json.load(reply[start:end])

    except:
        return {
            "goal":"chat",
            "conversation_type":"normal",
            "use_memory":True,
            "use_tools":False,
            "tool":"",
            "continue_topic":True,
            "ask_followup":False
        }