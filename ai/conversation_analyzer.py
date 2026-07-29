import requests
import json
from config import MODEL, OLLAMA_URL

def analyze_conversation(user_input):

    prompt=f"""
Du bist der Gesprächsanalysator von Nova.

Analysiere die Nachricht.

Antworte ausschließlich als JSON.

Schema:

{{
    "type":"",
    "emotion":"",
    "should_ask_question":false,
    "should_encourage":false,
    "should_use_memory":false,
    "answer_length":""
}}

Mögliche type:

chat
coding
question
learning
personal
command

Mögliche emotion:

neutral
happy
sad
angry
frustrated
exited

Mögliche answer_length:

short
medium
long

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

        return json.loads(reply[start:end])

    except:

        return{
            "type":"chat",
            "emotion":"neutral",
            "should_ask_question":False,
            "should_encourage":False,
            "should_use_memory":False,
            "answer_length":"medium"
        }