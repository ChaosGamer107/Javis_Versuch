import json
import requests
from config import MODEL, OLLAMA_URL

def create_plan(user_input):

    prompt="""
Du bist der interne Planer von Nova.

Analysiere die Nachricht.

Antworte ausschließlich als JSON.

Schema:

{{
    "goal":"",
    "needs_tool":false,
    "tool":"",
    "memory_needed":false,
    "should_ask_question":false,
    "conversation_type":""
}}

Nachricht:

{user_input}
"""
    response=requests.post(
        OLLAMA_URL,
        json={
            "model":MODEL,
            "prompt":prompt,
            "stream":False
        }
    )

    reply=response.json()["response"]

    try:
        start=reply.find("{")
        end=reply.find("}")+1

        return json.load(reply[start:end])

    except:
        return {
            "goal":"",
            "needs_tool":False,
            "tool":"",
            "memory_needed":False,
            "should_aks_question":False,
            "conversation_type":"normal"
        }