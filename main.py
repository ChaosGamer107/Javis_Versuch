from speech.speech import listen, speak
from memory.memory import init_db
from ai.brain import process
from tools.tool_registry import get_tool

init_db()

print("Nova ist bereit!")

while True:

    user_input=listen()

    if not user_input:
        continue

    if user_input.lower() in ["beenden", "stopp", "exit"]:
        break

    print("open_app:", get_tool("open_app"))

    reply=process(user_input)

    print("Nova:", reply)

    speak(reply)