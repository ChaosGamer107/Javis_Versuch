import threading
import gui
from tools.loader import load_tools
from speech.speech import listen, speak
from memory.memory import init_db
from ai.brain import process
from tools.tool_registry import get_tool
from apps.apps import load_programs

load_programs()

load_tools()

init_db()

print("Nova ist bereit!")

def nova_loop():

    while True:

        user_input=listen()

        if not user_input:
            continue

        if user_input.lower() in ["beenden", "stopp", "exit"]:
            break

        reply=process(user_input)

        print("Nova:", reply)

        speak(reply)

threading.Thread(target=nova_loop, daemon=True).start()
print("Öffne Fenster...")
gui.run()
