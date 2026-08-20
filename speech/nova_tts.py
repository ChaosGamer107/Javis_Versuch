import torch
import soundfile as sf
import pygame
import os
import time
import re
from pathlib import Path
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

REFERENCE_AUDIO = r"D:\KIs\Nova\speech\nova_voice_tests\nova_reference.wav"

OUTPUT_DIR = Path(r"D:\KIs\Nova\speech\nova_tts")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("Lade Nova TTS auf die GPU...")

device="cuda" if torch.cuda.is_available() else "cpu"

print(f"Verwendetes Gerät: {device}")

model=ChatterboxMultilingualTTS.from_pretrained(
    device=device,
    t3_model="v3"
)

model.prepare_conditionals(
    REFERENCE_AUDIO,
    exaggeration=0.5
)

print("Nova TTS bereit.")

pygame.mixer.init()

voice_id=0

def split_text(text):

    text=text.strip()

    if not text:
        return[]

    sentences=re.split(
        r'(?<=[.!?])\s+',
        text
    )

    sentences=[
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    return sentences


def speak_sentence(text):

    global voice_id

    if not text or not text.strip():
        return

    wav=model.generate(
        text,
        language_id="de",
        exaggeration=0.5,
        cfg_weight=0.5,
        temperature=0.8,
        repetition_penalty=2.0,
        min_p=0.05,
        top_p=1.0
        )

    audio=wav.detach().cpu().numpy()

    if audio.ndim == 2 and audio.shape[0] == 1:
            audio=audio[0]

    audio=audio.reshape(-1, 1)

    filename=OUTPUT_DIR / f"nova_{voice_id}.wav"

    voice_id+=1

    sf.write(
        str(filename),
        audio,
        model.sr
    )

    pygame.mixer.music.load(str(filename))
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.05)

    pygame.mixer.music.unload()

    try:
        os.remove(filename)
    except OSError:
        pass


def speak(text):

    if not text or not text.strip():
          return

    text=text.strip()

    sentences=split_text(text)

    for sentence in sentences:

        try:

            speak_sentence(sentence)

        except Exception as error:

            print("Fehler bei Nova TTS:")
            print(error)

        