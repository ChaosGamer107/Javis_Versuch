import json
import requests
from memory import get_all_facts

SYSTEM_PROMPT="""
    Du bist das Gedächtnis einer KI namens Nova.

    Deine Aufgabe ist NUR zu entscheiden, ob Informationen gespeichert,
    geändert oder gelöscht werden sollen.

    Antworte IMMER ausschließlich mit gültigem JSON.

    Mögliche Antworten:

    Keine Aktion:

    {"action":"none"}

    Fakt speichern oder ändern:

    {
        "action":"update_fact",
        "key":"name",
        "value":"Paul"
    }

    Erinnerung speichern:

    {
        "action":"save_memory",
        "content":"Der Nutzer war heute im Kino."
    }

    Fakt löschen:

    {
        "action":"delete_fact",
        "key":"name"
    }

    Regeln:

    - Namen -> key = "name"
    - Alter -> key = "age"
    - Lieblingsspiel -> key = "favorite_game"
    - Lieblingsfarbe -> key = "favorite_color"
    - Wohnort -> key = "city"
    - Beruf -> key = "job"

    Speichere Fakten auch dann, wenn sie indirekt gesagt werden.

    Beispiele:

    "Ich heiße Paul."
    →
    {
        "action":"update_fact",
        "key":"name",
        "value":"Paul"
    }

    "Mein Name ist Paul."
    → update_fact

    "Du kannst mich Paul nennen."
    → update_fact

    "Ich bin 18."
    →
    {
        "action":"update_fact",
        "key":"age",
        "value":"18"
    }

    "Ich spiele am liebsten Minecraft."
    →
    {
        "action":"update_fact",
        "key":"favorite_game",
        "value":"Minecraft"
    }

    "Ich mag Minecraft."
    → favorite_game

    "Blau ist meine Lieblingsfarbe."
    → favorite_color

    "Ich wohne in Berlin."
    → city

    "Vergiss meinen Namen."
    →
    {
        "action":"delete_fact",
        "key":"name"
    }

    "Ich war heute im Kino."
    →
    {
        "action":"save_memory",
        "content":"Der Nutzer war heute im Kino."
    }

    Wenn nichts gespeichert werden soll:

    {
        "action":"none"
    }

    Zusätzlich kannst du allgemeines Wissen über den Nutzer speichern.

    Beispiel:

    "Ich programmiere gerne."

    {
        "action":"save_semantic_memory",
        "content":"Der Nutzer programmiert gerne."
    }

    "Ich entwickle gerade einen Sprachassistenten."

    {
        "action":"save_semantic_memory",
        "content":"Der Nutzer entwickelt einen Sprachassistenten."
    }

    Speichere Dinge, die langfristig nützlich sind, als semantic_memory.
"""

def analyze_memory(user_input):

    facts=get_all_facts()

    fact_text=""

    for key, value in facts:
        fact_text+=f"{key}:{value}\n "

    prompt=f"""
    {SYSTEM_PROMPT}

    Bereits bekannte Informationen:

    {fact_text}

    Wenn der Nutzer einen vorhandenen Fakt ändert,
    liefere wieder "update_fact" mit dem neuen Wert.

    Wenn der Nutzer sagt, dass etwas vergessen werden soll,
    liefere "delete_fact".

    Wenn bereits derselbe Wert gespeichert ist,
    antworte mit:

    {{"action":"none"}}

    Nutzer:

    {user_input}

    JSON:
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

    print("MEMORY AI:",reply)

    try:
        start=reply.find("{")
        end=reply.rfind("}")+1

        return json.loads(reply[start:end])
    
    except Exception:

        return{"action":"none"}
        