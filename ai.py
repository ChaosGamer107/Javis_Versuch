import requests
import json

conversation = [
"""
Du bist Nova.

Bei normalen Gesprächen:
→ normale deutsche Antwort
"""
]

def ask_llama(user_input):

    conversation.append(f"Du: {user_input}")

    full_prompt="\n".join(conversation[-10:])+"\nNova:"

    response=requests.post( 
        "http://localhost:11434/api/generate",
        json={
            "model":"llama3",
            "prompt":full_prompt,
            "stream":False
        }
        )
    
    data=response.json()

    reply=data["response"].strip()

    conversation.append(f"Nova: {reply}")

    return reply


