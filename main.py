import requests
from datetime import datetime
import webbrowser
import json
import speech_recognition as sr
import pygame
import time
import os
from win32com.client import Dispatch

programs={}

start_menu_paths = [
    r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
    os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs")
]

shell=Dispatch("WScript.Shell")

for start_menu in start_menu_paths:

    for root, dirs, files in os.walk(start_menu):
        for file in files:
            if file.endswith(".lnk"):

                path=os.path.join(root,file)

                try:
                    shortcut=shell.CreateShortCut(path)

                    name=file.replace(".lnk", "").lower()

                    programs[name]=path

                except Exception as e:
                    print("Fehler:",e)
                    

pygame.mixer.init()

voice_id=0

print("Nova ist bereit")

conversation = [
"""
Du bist eine KI namens Nova.

WENN der Nutzer:
- ein Programm öffnen will
- Youtube öffnen will
- die Uhrzeit wissen will

Dann antworte NUR mit JSON.

Beispiele:

{"action":"time"}

{"action":"youtube"}

{"action":"open_app","app":"spotify"}

WICHTIG:
- KEIN zusätzlicher Text
- NUR JSON
- keine Erklärungen

Bei normalen Gesprächen:
→ normale Antwort auf Deutsch
"""
]

def open_app(app_name):
    
    app_name=app_name.lower()

    for program in programs:
        
        if app_name in program:

            print("Gefunden:",program)
            print("Pfad:",program[programs])

            try:
               os.startfile(programs[program])
               print("Gestartet")
               return f"Ich öffne {program}"
                
            except Exception as e:
               print("STARTFEHLER:", e)
               return "Fehler beim öffnen"
            
    return "Programm nicht gefunden"
    


def speak(text):

    global voice_id

    url ="https://api.elevenlabs.io/v1/text-to-speech/BnNQr9Ga1RxUGlZEeAoa"

    headers={
        "xi-api-key":"sk_eb3b1f8943208773108aefe8456301426c4746273f297efc",
        "Content-Type":"application/json"
    }

    data={
        "text":text,
        "voice_settings":{
            "stability":0.5,
            "similarity_boost":0.7
        }
    }

    response=requests.post(url, json=data, headers=headers)

    filename=f"voice_{voice_id}.mp3"
    voice_id += 1

    with open(filename,"wb") as f:
        f.write(response.content)

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
        
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
        audio=recognizer.listen(source, phrase_time_limit=5)

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
    print("DEBUG REPLY:", reply)

    result = None

    if any(word in user_input.lower() for word in ["uhr", "zeit", "spät"]):
        result = get_time()

    elif "{" in reply:
        try:
            start = reply.find("{")
            end = reply.rfind("}") + 1
            json_str = reply[start:end]

            parsed = json.loads(json_str)
            action = parsed.get("action")

            if action == "youtube":
                result = open_youtube()
                print("Nova:",result)
                speak(result)

            if action == "open_app":
                app=parsed.get("app")
                result=open_app(app)
                print("Nova:",result)
                speak(result)

        except Exception as e:
            print("Fehler:",e)
                


    if result is None:
        result = reply

        conversation.append(f"Nova: {str(result)}")
        
        print("Nova:",result)
        speak(result)