import requests
import json
from memory import get_all_facts, get_recent_memories 

conversation = []

def ask_llama(user_input):

    global conversation

    facts=get_all_facts()

    fact_text=""

    for key, value in facts:
        fact_text+=f"{key}: {value}\n"

    memories=get_recent_memories()

    memory_text=""

    for memory in memories:
        memory_text+=f"-{memory[0]}\n"

    conversation.append(f"User: {user_input}")

    conversation_text="\n".join(conversation[-10])

    prompt=f"""
        Du bist Nova.

        Bekannte Informationen über den Nutzer:

        {fact_text}

        Letzte Erinnerungen:

        {memory_text}

        Antworte natürlich.
        Nutze die Informationen nur, wenn sie relevant sind.

        User:
        {user_input}

        Nova:
        """

    response=requests.post( 
        "http://localhost:11434/api/generate",
        json={
            "model":"llama3",
            "prompt":full_prompt,
            "stream":False
        }
        )
    
    reply=response.json()["response"].strip()

    conversation.append(f"Nova: {reply}")

    return reply

  

