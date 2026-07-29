import requests
import json
from memory import get_all_facts, get_recent_conversations, search_memories_semantic, add_conversation
from personality import build_personality
from tool_registry import get_tool_discription
from config import OLLAMA_URL, MODEL
from conversation_state import get_conversation_context
from reasoning import build_reasoning
from planner import create_plan
from conversation_analyzer import analyze_conversation
from brain import think

conversation = []

def ask_llama(user_input):

    tool_text=get_tool_discription()

    facts=get_all_facts(user_input)
    context=search_memories_semantic()
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

    
    conversation_context=get_conversation_context()

    brain=think(user_input)

    analysis=brain["analysis"]
    reasoning=brain["reasoning"]
    plan=brain["plan"]

    prompt=f"""

    {build_personality()}

    Gesprächsanalyse:

        Gesprächsart:
        {analysis["type"]}

        Emotion:
        {analysis["emotion"]}

        Rückfrage stellen:
        {analysis["should_ask_question"]}

        Memory benutzen:
        {analysis["should_use_memory"]}

        Antwortlänge:
        {analysis["answer_length"]}

    Interner Plan:

        Ziel:
        {plan["goal"]}

        Gesprächsart:
        {plan["conversation_type"]}

        Soll eine Rückfrage gestellt werden ?:
        {plan["should_ask_question"]}

        Nutze diesen Plan.

    {reasoning}

    {conversation_context} 
            
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
        OLLAMA_URL,
        json={
            "model":MODEL,
            "prompt":prompt,
            "stream":False
        }
        )
    
    reply=response.json()["response"].strip()

    add_conversation("User",user_input)
    add_conversation("Nova",reply)

    return reply

  

