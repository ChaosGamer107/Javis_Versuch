import json
from speech import listen, speak
from ai import ask_llama
from memory import init_db, add_memory, delete_fact, add_semantic_memory
from memory_ai import analyze_memory
import skills
from tool_registry import execute_tool
from conversation import analyze_conversation, save_last_question
from conversation_engine import improve_reply

print("Nova startet...")

init_db()

print("Nova ist bereit!")

while True:

    user_input=listen()

    analyze_conversation(user_input)

    if user_input.strip()=="":
        continue

    text = user_input.lower()

    if "exit" in text or "beenden" in text or "stopp" in text:
         break

    memory_action=analyze_memory(user_input)

    if memory_action["action"]=="update_fact":

        from memory import save_fact

        save_fact(
            memory_action["key"],
            memory_action["value"]
        )

        print("FACT gespeichert")

    elif memory_action["action"]=="save_memory":

        add_memory(
            "personal",
            memory_action["content"]
        )

        print("MEMORY gespeichert")

    elif memory_action["action"]=="delete_fact":

        delete_fact(memory_action["key"])

        print("FACT gelöscht")

    elif memory_action["action"]=="save_semantic_memory":

        add_semantic_memory(
            memory_action["content"]
        )

        print("SEMANTIC MEMORY gespeichert")
    
    reply=ask_llama(user_input)

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
