import json
from speech import listen, speak
from ai import ask_llama
from apps import open_app
from commands import get_time, open_youtube
from memory import init_db, add_memory, get_memories, search_memories, get_latest_memory

print("Nova ist bereit")

init_db()

while True:

    important_phrases=[
         "mein name ist",
        "ich wohne in",
        "mein lieblingsspiel ist",
        "meine lieblingsfarbe ist",
        "mein hund heißt",
        "meine katze heißt"
    ]

    for phrase in important_phrases:
        if phrase in text:
              
              add_memory(
                   "personal",
                   user_input
              )

              print("MEMORY GESPEICHERT")

        if "erinnerst du dich" in text:
         
         keyword=text.replace(
              "erinnerst du dich",
              ""
         ).strip()

        memories=search_memories(keyword)

        if memories:
            result=memories[0][0]
        else:
            result="Dazu habe ich nichts gespeichert."

        print("Nova:", result)
        speak(result)
        continue

    if any(word in text for word in ["uhr","zeit","spät"]):

        result=get_time()

        print("Nova:", result)
        speak(result)
        continue

    if "youtube" in text:

        result=open_youtube()

        print("Nova:", result)
        speak(result)
        continue

    if text.startswith("öffne"):

        app=text.replace("öffne","").strip()

        result=open_app()

        print("Nova:", result)
        speak(result)
        continue



    user_input=listen()

    user_input=listen()

    if user_input.strip() == "":
          continue

    text = user_input.lower()


    result = None
    action = None

    result = reply

    if "exit" in text or "beenden" in text or "stop" in text:
         print("Nova: Bis bald!")
         speak("Okay, ich fahre runter")
         break