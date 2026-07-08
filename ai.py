import requests
import json
from memory import get_all_facts, get_recent_conversations, get_relevant_context, add_conversation
from personality import build_personality
from tool_registry import get_tool_discription

conversation = []

def ask_llama(user_input):

    tool_text=get_tool_discription()

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

        Verfügbare Werkzeuge:

        {tool_text}

        Wenn ein Werkzeug benötigt wird,
        antworte ausschließlich mit JSON.

        Beispiel:

        {{"action":"time"}}

        {{"action":"open_app","app":"spotify"}}

        Bekannte Fakten:

        {fact_text}

        Relevante Informationen:

        {context_text}

        Letzte Unterhaltung:

        {conversation_text}

        User:

        {user_input}

        Nova:
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

  

