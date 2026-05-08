import requests
import pygame
import os
import time

pygame.mixer.init()

API_KEY = os.getenv("ELEVEN_API_KEY")

def speak(text):
    url = "https://api.elevenlabs.io/v1/text-to-speech/MGG5Irb57ATHvyIeTEYo"

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

    # 🔥 WICHTIG
    if response.status_code != 200:
        print("API Fehler:", response.status_code)
        print(response.text)
        return

    with open("voice.mp3", "wb") as f:
        f.write(response.content)

    pygame.mixer.music.load("voice.mp3")
    pygame.mixer.music.play()

    import time
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

speak("Systemprüfung abgeschlossen. Alle Funktionen arbeiten innerhalb der Parameter.")

print(response.headers.get("content-type"))