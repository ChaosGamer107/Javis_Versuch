import speech_recognition as sr
import pygame
import requests
import time
from config import ELEVENLABS_API_KEY, VOICE_ID, LANGUAGE, PHRASE_TIME_LIMIT

pygame.mixer.init()

voice_id=0

def listen():
    recognizer=sr.Recognizer()

    with sr.Microphone() as source:
        print("Ich höre...")
        audio=recognizer.listen(source, phrase_time_limit=PHRASE_TIME_LIMIT)

    try:
        text=recognizer.recognize_google(audio, language=LANGUAGE)
        print("Du:", text)
        return text
    except:
        print("Ich habe dich nicht verstanden")
        return ""
    
def speak(text):

    global voice_id

    url ="https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers={
        "xi-api-key":"ELEVENLABS_API_KEY",
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