import speech_recognition as sr
import pygame
import requests
import time
import os
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
    except sr.UnknownValueError:
        print("Ich habe dich nicht verstanden")
        return ""
    
def speak(text):

    global voice_id

    url ="https://api.elevenlabs.io/v1/text-to-speech/BnNQr9Ga1RxUGlZEeAoa"

    headers={
        "xi-api-key":ELEVENLABS_API_KEY,
        "Content-Type":"application/json"
    }

    data={
        "text":text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings":{
            "stability":0.5,
            "similarity_boost":0.7
        }
    }

    try:

        response=requests.post(url, json=data, headers=headers, timeout=30)

        if response.status_code != 200:

            print(
                "ElevenLabs Fehler:",
                response.status_code,
                response.text
            )

            return

        filename=f"voice_{voice_id}.mp3"
        voice_id += 1

        with open(filename,"wb") as file:
            file.write(response.content)

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.unload()

        os.remove(filename)

    except requests.RequestException as error:

        print(f"Fehler bei ElevenLabs:", {error})

    except pygame.error as error:

        print(f"Fehler beim Abspielen der Sprachausgabe:", {error})


