import requests
from datetime import datetime
import webbrowser
import json

print("Nova ist bereit")

conversation=[
    """Du bist eine KI namens Nova.

Wenn der User eine Aktion will, antworte nur in JSON:

{"action":"time"}
oder
{"action":"youtube"}

WICHTIG:
-kein extra Text
-Nur JSON
-Keine Erklärung

Wenn keine Aktion nötig ist:
-> Antworte normal
"""
]

def get_time():
    now = datetime.now()
    print("DEBUG SYSTEM TIME:", now)
    return f"Es ist {now.strftime('%H:%M:%S')} Uhr"

def open_youtube():
    webbrowser.open("https://www.youtube.com")
    return "Ich öffne Youtube"

while True:

    user_input=input("Du:")

    if user_input.lower() == "exit":
        print("Nova: Bis bald!")
        break

    conversation.append(f"Du: {user_input}")

    full_prompt="\n".join(conversation)+"\nNova:"

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

    result = None

    if any(word in user_input.lower() for word in ["uhr", "zeit", "spät"]):
        print("DEBUG: direkte Zeit")
        result = get_time()

    elif "{" in reply:
        try:
            start = reply.find("{")
            end = reply.rfind("}") + 1
            json_str = reply[start:end]

            print("DEBUG JSON:", json_str)

            parsed = json.loads(json_str)
            action = parsed.get("action")

            if action == "youtube":
                result = open_youtube()

        except:
            pass
                


if result is None:
    print("DEBUG: normale KI Antwort")
    result = reply

    conversation.append(f"Nova: {str(result)}")
        
    print("Nova:",result)