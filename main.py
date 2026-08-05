from speech.speech import listen, speak
from memory.memory import init_db
from ai.brain import process

init_db()

print("Nova ist bereit!")

while True:

    user_input=listen()

    if not user_input:
        continue

    if user_input.lower() in ["beenden", "stopp", "exit"]:
        break

    reply=process(user_input)

    print("Nova:", reply)

    speak(reply)