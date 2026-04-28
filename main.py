import requests
from datetime import datetime
import webbrowser
import json
import speech_recognition as sr
import pyttsx3

engine=pyttsx3.init()

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

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_time():
    now = datetime.now()
    print("DEBUG SYSTEM TIME:", now)
    return f"Es ist {now.strftime('%H:%M:%S')} Uhr"

def open_youtube():
    webbrowser.open("https://www.youtube.com")
    return "Ich öffne Youtube"

def listen():
    recognizer=sr.Recognizer()

    with sr.Microphone() as source:
        print("Ich höre...")
        audio=recognizer.listen(source)

    try:
        text=recognizer.recognize_google(audio, language="de-DE")
        print("Du:", text)
        return text
    except:
        print("Ich habe dich nicht verstanden")
        return ""

while True:

    user_input=listen()

    text = user_input.lower()

    if "exit" in text or "beenden" in text or "stop" in text:
        print("Nova: Bis bald!")
        speak("Okay, ich fahre runter")
        break

    if user_input.strip()=="":
        continue

    if any(word in user_input.lower() for word in ["uhr","zeit","spät"]):
        result=get_time()
        print("Nova:",result)
        speak(result)
        continue

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
    speak(result)