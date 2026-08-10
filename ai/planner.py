import json
import requests
from config import MODEL, OLLAMA_URL

def create_plan(user_input):

    prompt="""
Du bist Novas interner Aktionsplaner.

Analysiere die Nachricht des Users.

Antworte AUSSCHLIESSLICH als JSON.
KEIN Markdown.
KEINE Erklärung.
KEINE zusätzlichen Wörter.

Exaktes Schema:

{{
    "goal": "string",
    "conversation_type": "string",
    "use_memory": false,
    "use_tools": false,
    "tool": "",
    "arguments": {{}},
    "continue_topic": true,
    "ask_followup": false
}}

Regeln:

use_tools = true:
Nur wenn tatsächlich eine Aktion auf dem Computer ausgeführt werden soll.

tool:
Der exakte Name des Tools.

arguments:
Die benötigten Argumente für das Tool.

ask_followup = true:
Nur wenn eine für die Aufgabe notwendige Information fehlt.

Keine unnötigen Rückfragen.

Beispiele:

User: Öffne Spotify

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

User: Wie geht's dir?

{{
    "goal": "Smalltalk führen",
    "conversation_type": "chat",
    "use_memory": false,
    "use_tools": false,
    "tool": "",
    "arguments": {{}},
    "continue_topic": true,
    "ask_followup": false
}}

User: Ich arbeite gerade an Nova

{{
    "goal": "Gespräch über Nova fortführen",
    "conversation_type": "chat",
    "use_memory": true,
    "use_tools": false,
    "tool": "",
    "arguments": {{}},
    "continue_topic": true,
    "ask_followup": false
}}

User:
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

        start=raw.find("{")
        end=raw.find("}")+1

        if start == -1 or end <= start:
            raise ValueError("Planner hat kein JSON zurückgegeben: {raw}")

        raw=raw[start:end]

        try:

            plan=json.loads(raw)

        except json.JSONDecodeError:

            plan=ast.literal_eval(raw)

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





Nova ist bereit!
Ich höre...
Du: wie geht's dir
Planner-Fehler: name 'ast' is not defined
Nova: Hallo! Ich bin Nova, deine persönliche KI-Assistentin. Ich bin gut gelaunt und freue mich, dass wir uns sprechen. Wie kann ich dich heute unterstützen?
Ich höre...
Du: öffne Spotify
Planner-Fehler: name 'ast' is not defined
Nova: Hallo! Ich verstehe, dass du mich bitten möchtest, Spotify zu öffnen. Ich bin bereit, diese Aktion auszuführen. Ich gebe dir nun den Befehl: "öffne Spotify".
Ich höre...
Du: Stopp