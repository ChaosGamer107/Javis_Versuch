import json
import requests
from config import MODEL, OLLAMA_URL

def create_plan(user_input):

    prompt="""
Analysiere diese Benutzeranfrage und entscheide, ob ein Tool ausgeführt werden muss.

Antworte ausschließlich mit einem einzigen gültigen JSON-Objekt.
Keine Erklärung.
Kein Markdown.
Keine zusätzlichen Zeichen.

Schema:

{{
  "goal": "",
  "conversation_type": "",
  "use_memory": false,
  "use_tools": false,
  "tool": "",
  "arguments": {{}},
  "continue_topic": true,
  "ask_followup": false
}}

Regeln:

- use_tools = true nur wenn eine Aktion auf dem Computer ausgeführt werden soll.
- tool muss der exakte Toolname sein.
- arguments enthält die Argumente des Tools.
- ask_followup = true nur wenn eine notwendige Information fehlt.
- Bei eindeutigem Befehl niemals nachfragen.

Beispiel:

Benutzer: Öffne Spotify

Antwort:
{{"goal":"Spotify öffnen","conversation_type":"command","use_memory":false,"use_tools":true,"tool":"open_app","arguments":{{"app_name":"Spotify"}},"continue_topic":false,"ask_followup":false}}

Benutzer: Wie geht's dir?

Antwort:
{{"goal":"Smalltalk","conversation_type":"chat","use_memory":false,"use_tools":false,"tool":"","arguments":{{}},"continue_topic":true,"ask_followup":false}}

Benutzer:
{user_input}
"""

    try:

        response=requests.post(
            OLLAMA_URL,
            json={
                "model":MODEL,
                "prompt":prompt,
                "format":"json",
                "stream":False,
                "options":{
                    "temperature":0
                },
                "keep_alive":"10m"
            },
            timeout=60
        )

        response.raise_for_status()

        raw=response.json()["response"].strip()

        print("Planner:", raw)

        plan=json.loads(raw)

        return normalize_plan(plan)

    except Exception as error:

        print(f"Planner-Fehler: {error}")
        
        return {
            "goal": "Normales Gespräch",
            "conversation_type": "chat",
            "use_memory": False,
            "use_tools": False,
            "tool": "",
            "arguments": {},
            "continue_topic": True,
            "ask_followup": False
        }

def normalize_plan(plan):

    return {
        "goal": plan.get("goal", ""),
        "conversation_type": plan.get(
            "conversation_type",
            "normal"
        ),
        "use_memory": bool(
            plan.get("use_memory", False)
        ),
        "use_tools": bool(
            plan.get("use_tools", False)
        ),
        "tool": plan.get("tool", ""),
        "arguments": plan.get(
            "arguments",
            {}
        ),
        "continue_topic": bool(
            plan.get("continue_topic", True)
        ),
        "ask_followup": bool(
            plan.get("ask_followup", False)
        )
    }





