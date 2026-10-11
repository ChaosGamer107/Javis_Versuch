import numpy as np
import gui
import speech_recognition as sr
import torch
import soundfile as sf
import pygame
import os
import time
import re
import threading
import queue
from pathlib import Path
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
from config import LANGUAGE, PHRASE_TIME_LIMIT

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

recognizer=sr.Recognizer()
recognizer.pause_threshold = 1.2

_calibrated=False

def _make_spectrum(filename, band_count, window_size=2048):

    data, sample_rate=sf.read(str(filename))

    if data.ndim > 1:
        data=data.mean(axis=1)

    if len(data) < window_size:
        data=np.pad(data, (0, window_size-len(data)))

    hop=sample_rate//60

    windows=np.lib.stride_tricks.sliding_window_view(data, window_size)[::hop]
    windows=windows*np.hanning(window_size)

    magnitude=np.abs(np.fft.rfft(windows, axis=1))

    freqs=np.fft.rfftfreq(window_size, 1/sample_rate)
    edges=np.geomspace(100, 7000, band_count+1)

    bands=np.zeros((len(magnitude), band_count))

    for b in range(band_count):

        mask=(freqs >= edges[b]) & (freqs < edges[b+1])

        if not mask.any():

            mask=np.zeros(len(freqs), dtype=bool)
            mask[np.argmin(np.abs(freqs-(edges[b]+edges[b+1])/2))]=True

        bands[:, b]=magnitude[:, mask].mean(axis=1)

    scale=np.maximum(np.percentile(bands, 95, axis=0), bands.max()*0.05)+1e-9
    bands=np.clip(bands/scale, 0, 1)*0.8

    return bands, hop/sample_rate

def listen():

    global _calibrated

    with sr.Microphone() as source:

        if not _calibrated:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            _calibrated=True
            print(f"Mikrofon kalibriert, Schwellwert: {recognizer.energy_threshold:.0f}")

        print("Ich höre...")   
        
        try:
            gui.set_mode("listening")

            audio=recognizer.listen(source, timeout=10, phrase_time_limit=PHRASE_TIME_LIMIT)

        except sr.WaitTimeoutError:
            return ""

    try:

        t0=time.time()

        text=recognizer.recognize_faster_whisper(
            audio, 
            model="medium",
            init_options={"device":"cuda", "compute_type":"float16"},
            language=LANGUAGE,
            initial_prompt="Nova, öffne Spotify. Merk dir, das ich Volleyball mag. Wie spät ist es ?"
        ).strip()

        print(time.time()-t0)
        
        print("Du:", text)
        gui.set_text(text)
        gui.set_mode("thinking")
        return text

    except sr.UnknownValueError:
        print("")
    

    except sr.RequestError as error:
        print("Spracherkennung Fehler:", error)
        return ""

def split_text(text):

    text=text.strip()

    if not text:
        return[]

    text = re.sub(r"\s+", " ", text)

    sentences=re.split(
        r"(?<=[.!?])\s+",
        text
    )

    sentences=[
        s.strip()
        for s in sentences
        if s.strip()
    ]

    chunks=[]

    current= ""

    for sentence in sentences:

        if len(sentence) > 250:
            words=sentence.split()
            current=""

            for word in words:
                candidate=(
                    word
                    if not current
                    else current + " " + word
                )

                if len(candidate)<=250:
                    current=candidate
                else:
                    if current:
                        chunks.append(current)

                    current=word

            if current:
                chunks.append(current)

            current=""
            continue

        if not current:
            current=sentence
            continue

        candidate=current + " " + sentence

        if len(candidate)<=250:
            current=candidate
        else:
            chunks.append(current)
            current=sentence

    if current:
        chunks.append(current)

    return chunks

def calculate_max_tokens(text):

    characters=len(text)
    words=len(text.split())

    estimated=int(
        characters*1.35
    )

    estimated=max(
        estimated,
        80
    )

    estimated+=25

    estimated=min(
        estimated,
        450
    )

    print(
        f"TTS-Limit: {estimated} Speech-Tokens"
        f"für {words} Wörter / {characters} Zeichen"
    )

    return estimated

def generate_audio(text):

    print("DEBUG generate_audio:", repr(text))

    t_start=time.time()

    text=text.strip()

    text=text.strip()

    if not text:
        return None

    from chatterbox.mtl_tts import punc_norm

    original_text=text

    text=punc_norm(text)
    text = re.sub(r"\s+", " ", text).strip()

    print(f"TTS ORIGINAL: '{original_text}'")
    print(f"TEXT VOR TOKENIZER: '{text}'")

    text_tokens=model.tokenizer.text_to_tokens(
        text,
        language_id="de"
    ).to(model.device)

    sot=model.t3.hp.start_text_token
    eot=model.t3.hp.stop_text_token

    text_tokens=torch.nn.functional.pad(
        text_tokens,
        (1, 0),
        value=sot
    )

    text_tokens=torch.nn.functional.pad(
        text_tokens,
        (0, 1),
        value=eot
    )

    text_tokens=torch.cat(
        [text_tokens, text_tokens],
        dim=0
    )

    max_tokens=calculate_max_tokens(text)

    if device == "cuda":
        torch.cuda.synchronize()
    t_tokenize=time.time()

    with torch.inference_mode():

        speech_tokens=model.t3.inference(
            t3_cond=model.conds.t3,
            text_tokens=text_tokens,
            max_new_tokens=max_tokens,
            stop_on_eos=True,
            temperature=0.7,
            cfg_weight=0.55,
            repetition_penalty=1.3,
            min_p=0.08,
            top_p=0.9
        )

    if device == "cuda":
        torch.cuda.synchronize()
    t_t3=time.time()

    speech_tokens=speech_tokens[0]

    speech_tokens=speech_tokens[speech_tokens < 6561]

    if speech_tokens.numel() == 0:
        print("Keine gültigen Speech-Tokens erzeugt.")
        return None

    print(
        f"Speech-Tokens: {speech_tokens.numel()}"
        f"Max: {speech_tokens.max().item()} / Limit: {max_tokens}"
    )

    with torch.inference_mode():

        wav=model.s3gen.inference(
            speech_tokens=speech_tokens,
            ref_dict=model.conds.gen
        )

    if device == "cuda":
        torch.cuda.synchronize()
    t_s3gen=time.time()

    if isinstance(wav, tuple):

        wav=wav[0]

    if torch.is_tensor(wav):

        audio=(wav.squeeze().detach().cpu().numpy())

    else:

        audio=wav.squeeze()

    audio=model.watermarker.apply_watermark(
        audio,
        model.sr
    )

    t_watermark = time.time()

    print(
        f"[TIMING] Tokenize: {t_tokenize - t_start: .2f}s |"
        f"T3: {t_t3 - t_tokenize: .2f}s |"
        f"S3Gen: {t_s3gen - t_t3: .2f}s |"
        f"Watermark: {t_watermark - t_s3gen: .2f}s |"
        f"Gesamt: {t_watermark - t_start: .2f}s |"
    )

    print(next(model.t3.parameters()).dtype)

    return audio

def save_audio(audio):

    global voice_id

    if audio is None:
        return None

    filename=OUTPUT_DIR / f"nova_{voice_id}.wav"

    voice_id+=1

    sf.write(
        str(filename),
        audio,
        model.sr
    )

    return filename

def play_audio(filename):

    if filename is None:
        return 

    bands, step=_make_spectrum(filename, gui.NUM_BANDS)

    pygame.mixer.music.load(str(filename))
    pygame.mixer.music.play()

    gui.set_mode("speaking")

    while pygame.mixer.music.get_busy():

        index=int(pygame.mixer.music.get_pos()/1000/step)

        if 0 <= index < len(bands):
            gui.set_bands(bands[index])

        time.sleep(0.02)

    gui.set_bands(None)

    pygame.mixer.music.unload()

    try:
        os.remove(filename)
    except OSError:
        pass

def speak(text):

    if not text or not text.strip():
          return

    chunks=split_text(text)

    if not chunks:
        return

    print(f"Nova TTS: {len(chunks)} Audioblock/Blöcke")

    audio_queue=queue.Queue()

    generation_finished=threading.Event()

    generation_failed=threading.Event()

    def producer():

        try:

            for index,chunk in enumerate(chunks):

                print()
                print(
                    f"[TTS {index + 1}/{len(chunks)}]"
                )

                generated_audio=generate_audio(chunk)

                if generated_audio is None:

                    print(
                        f"[TTS {index + 1}]"
                        "Keine Audiodaten erhalten."
                    )

                    continue

                filename=save_audio(
                    generated_audio
                )

                if filename is None:

                    print(
                        f"[TTS {index + 1}]"
                        "Audio konnte nicht gespeichert werden."
                    )

                    continue

                audio_queue.put(filename)

                print(
                    f"[TTS {index + 1}]"
                    "Audio bereit."
                )

        except Exception as error:

            generation_failed.set()

            print()
            print("Fehler im TTS Producer.")
            print(type(error).__name__, ":", error)

            import traceback
            traceback.print_exc()

        finally:

            generation_finished.set()

    worker=threading.Thread(
        target=producer,
        daemon=True
    )

    worker.start()

    while True:

        try:

            filename=audio_queue.get(
                timeout=0.1
            )

        except queue.Empty:

            if generation_finished.is_set():

                break

            continue

        try:

            play_audio(filename)

        finally:

            audio_queue.task_done()

    worker.join()

    if generation_failed.is_set():

        print()
        print("Nova TTS wurde wegen eines Generierungsfehler abgebrochen.")

    else:

        print()
        print("Nova TTS fertig.")

