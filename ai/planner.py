import json
import requests
from config import MODEL, OLLAMA_URL

def create_plan(user_input, tool_text):

    prompt="""
Du bist der Tool-Router einer persönlichen KI.

Deine EINZIGE Aufgabe ist zu entscheiden:
1. Braucht die Benutzeranfrage ein Tool?
2. Falls ja: Welches der verfügbaren Tools?
3. Welche Argumente benötigt dieses Tool?

VERFÜGBARE TOOLS:

{tool_text}

WICHTIGE REGELN:

REGEL 1:
Wenn der Benutzer nur mit Nova redet, darf KEIN Tool verwendet werden.

Beispiele:
"Wie geht's dir?"
"Hallo"
"Was denkst du darüber?"
"Erzähl mir etwas"
"Was ist Python?"

Bei solchen Nachrichten:

"use_tools": false
"tool": ""
"arguments": {{}}

REGEL 2:
get_time darf AUSSCHLIESSLICH verwendet werden,
wenn der Benutzer nach der aktuellen Uhrzeit fragt.

Beispiele:
"Wie spät ist es?"
"Wie viel Uhr ist es?"
"Welche Uhrzeit haben wir?"
"Wie spät haben wir es?"

get_time darf NICHT verwendet werden bei:
"Wie geht's dir?"
"Was machst du?"
"Öffne Spotify"
"Starte Spotify"

REGEL 3:
open_app darf AUSSCHLIESSLICH verwendet werden,
wenn der Benutzer eine Anwendung auf dem Computer öffnen
oder starten möchte.

Beispiele:
"Öffne Spotify"
"Starte Spotify"
"Mach Spotify auf"

Dann muss gelten:

"tool": "open_app"

und:

"arguments": {{
    "app_name": "Spotify"
}}

Das Verb "öffne", "öffnen", "starte", "starten", "mach auf"
gehört NICHT zu app_name.

REGEL 4:
Wenn kein Tool eindeutig benötigt wird:

"use_tools": false

REGEL 5:
Verwende ausschließlich Tools aus der Liste
"VERFÜGBARE TOOLS".

REGEL 6:
Erfinde niemals ein Tool.

REGEL 7:
Stelle keine Rückfrage, wenn die Anfrage eindeutig ist.

Antworte ausschließlich mit einem einzigen gültigen JSON-Objekt.

Schema:

{{
    "goal": "kurze Beschreibung",
    "conversation_type": "chat oder command",
    "use_memory": false,
    "use_tools": false,
    "tool": "",
    "arguments": {{}},
    "continue_topic": true,
    "ask_followup": false
}}

TESTBEISPIELE:

Eingabe:
Wie geht's dir?

Ausgabe:
{{
    "goal": "Smalltalk",
    "conversation_type": "chat",
    "use_memory": false,
    "use_tools": false,
    "tool": "",
    "arguments": {{}},
    "continue_topic": true,
    "ask_followup": false
}}

Eingabe:
Öffne Spotify

Ausgabe:
{{
    "goal": "Spotify öffnen",
    "conversation_type": "command",
    "use_memory": false,
    "use_tools": true,
    "tool": "open_app",
    "arguments": {{
        "app_name": "Spotify"
    }},
    "continue_topic": false,
    "ask_followup": false
}}

Eingabe:
Wie spät ist es?

Ausgabe:
{{
    "goal": "Aktuelle Uhrzeit ermitteln",
    "conversation_type": "command",
    "use_memory": false,
    "use_tools": true,
    "tool": "get_time",
    "arguments": {{}},
    "continue_topic": false,
    "ask_followup": false
}}

Eingabe:
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





