import speech_recognitonition as sr
import pygame

pygame.mixer.init()

voice_id=0

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