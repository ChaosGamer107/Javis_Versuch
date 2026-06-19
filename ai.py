import requests

conversation = [
"""
Du bist Nova.

WENN eine Aktion nötig ist,
antworte AUSSCHLIESSLICH mit gültigem JSON.

ERLAUBTE FORMATE:

{"action":"time"}

{"action":"youtube"}

{"action":"open_app","app":"spotify"}

WICHTIG:
- Nur gültiges JSON
- Keine Erklärungen
- Kein extra Text
- Kein Markdown
- Keine Emojis
- Keine Kommentare

Bei normalen Gesprächen:
→ normale deutsche Antwort
"""
]

def aks_llama(user_input):

    response=requests.post( 
        "http://localhost:11434/api/generate",
        json={
            "model":"llama3",
            "prompt":full_prompt,
            "stream":False
        }
        )
    
    data=response.json()

    return data["response"].strip()

full_prompt="\n".join(conversation[-10:])+"\nNova:"

