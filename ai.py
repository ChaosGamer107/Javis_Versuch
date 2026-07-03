import requests
import json
from memory import get_all_facts, get_recent_conversations, get_relevant_context, add_conversation
from personality import build_personality

conversation = []

def ask_llama(user_input):

    global conversation

    facts=get_all_facts()
    context=get_relevant_context()
    conversations=get_recent_conversations()

    fact_text=""

    for key, value in facts:
        fact_text+=f"{key}: {value}\n"


    context_text=""

    for item in context:
        context_text+=f"-{item}\n"


    conversation_text=""

    for speaker, message in conversations:
        conversation_text+=f"{speaker}:{message}\n"

    

    prompt=f"""
       {build_personality()}

        Bekannte Fakten:

        ...
        """

    response=requests.post( 
        "http://localhost:11434/api/generate",
        json={
            "model":"llama3",
            "prompt":prompt,
            "stream":False
        }
        )
    
    reply=response.json()["response"].strip()

    add_conversation("User",user_input)
    add_conversation("Nova",reply)

    return reply

  

