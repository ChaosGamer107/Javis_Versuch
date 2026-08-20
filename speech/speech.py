import speech_recognition as sr
from config import LANGUAGE, PHRASE_TIME_LIMIT
from speech.nova_tts import speak

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