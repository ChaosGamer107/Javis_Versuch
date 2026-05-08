import requests
import pygame
import time

pygame.mixer.init()

API_KEY = "sk_eb3b1f8943208773108aefe8456301426c4746273f297efc"

def speak(text):
    url = "https://api.elevenlabs.io/v1/text-to-speech/BnNQr9Ga1RxUGlZEeAoa"

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.45,
            "similarity_boost": 0.75,
            "style": 0.3,
            "use_speaker_boost": True
        }
    }

    response = requests.post(url, json=data, headers=headers)

    print("Content-Type:", response.headers.get("content-type"))

    if response.status_code != 200:
        print("API Fehler:", response.status_code)
        print(response.text)
        return

    with open("voice.mp3", "wb") as f:
        f.write(response.content)

    pygame.mixer.music.load("voice.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

speak("Systemprüfung abgeschlossen. Alle Funktionen arbeiten innerhalb der Parameter.")