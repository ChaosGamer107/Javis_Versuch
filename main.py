import json
import speech_recognition as sr
import time
from win32com.client import Dispatch
from memory import init_db, add_memory, get_memories, search_memorie

print("Nova ist bereit")

init_db

while True:

    user_input=listen()

    important_phrases=[
        "mein name ist",
        "ich wohne in",
        "mein Lieblingspiel ist",
        "meine lieblingsfarbe ist",
        "mein hund heißt",
        "meine katze heißt"
    ]

    for phrase in important_phrases:
        if phrase in user_input.lower():

            add_memory(
                "personal",
                user_input
            )

            print("MEMORY GESPEICHERT")

    text = user_input.lower()

   

    result = None
    action = None

    if "{" in reply:

        try:
            start = reply.find("{")
            end = reply.rfind("}")+1

            json_str = reply[start:end]
            json_str = json_str.replace("'", '"')
            print("JSON STRING:", json_str)
            parsed = json.loads(json_str)
            action = parsed.get("action")
            print("ACTION:",action)

            if action is None:
                print("UNBEKANNTE JSON ANTWORT")

            if action == "youtube":
                result = open_youtube()
                print("Nova:",result)
                speak(result)
                conversation.append(f"Nova hat Youtube geöffnet.")
                continue

            if action == "time":
                result = get_time()
                print("Nova:",result)
                speak(result)
                conversation.append(f"Nova hat die Zeit angegeben.")
                continue

            elif action == "open_app":
                app = parsed.get("app")
                result = open_app(app)
                print("Nova:",result)
                speak(result)
                conversation.append(f"Nova hat erfolgreich {app} geöffnet.")
                continue

        except Exception as e:
            print("Fehler:", e)


        result = reply

        if not reply.startswith("{"):
            print("Nova:",reply)
            speak(reply)