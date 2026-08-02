import json
from speech import listen, speak
from ai.ai import ask_llama
from memory import init_db, add_memory, delete_fact, add_semantic_memory, save_fact
from ai.memory_ai import analyze_memory
import skills
from Tools.tool_registry import execute_tool
from memory.conversation import save_last_question, update_conversation
from ai.conversation_engine import improve_reply
from ai.response_generator import improve_response

print("Nova startet...")

init_db()

print("Nova ist bereit!")

while True:

    user_input=listen()

    if user_input.strip()=="":
        continue

    text = user_input.lower()

    if "exit" in text or "beenden" in text or "stopp" in text:
         break

    memory_action=analyze_memory(user_input)

    if memory_action["action"] == "update_fact":

        save_fact(
            memory_action["key"],
            memory_action["value"]
        )

        message = f"Alles klar. Ich merke mir: {memory_action['key']} = {memory_action['value']}."

        print("Nova:", message)
        speak(message)

    elif memory_action["action"] == "save_memory":

        add_memory(
            "personal",
            memory_action["content"]
        )

        message = "Okay, das merke ich mir."

        print("Nova:", message)
        speak(message)

    elif memory_action["action"] == "delete_fact":

        delete_fact(
            memory_action["key"]
        )

        message = f"Alles klar. Ich habe {memory_action['key']} vergessen."

        print("Nova:", message)
        speak(message)
    
    reply=ask_llama(user_input)

    update_conversation(
        user_input,
        reply
    )

    speak(reply)

    reply=improve_response(
        user_input,
        reply
    )

    reply=improve_reply(user_input, reply)

    print("DEBUG:",reply)

    if reply.startwith("{"):

        try:

            parsed=json.loads(reply)

            action=parsed["action"]

            arguments=parsed.copy()
            arguments.pop("action",None)

            result=execute_tool(action,arguments)

            print(result)
            speak(result)

            continue

        except Exception as e:

            print("JSON Fehler:",e)

    print("Nova:", reply)
    speak(reply)

    if "?" in reply:
        save_last_question(reply)
