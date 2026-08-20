import torch
import torchaudio as ta
from pathlib import Path
import soundfile as sf

from chatterbox.mtl_tts import ChatterboxMultilingualTTS

REFERENCE_AUDIO = r"D:\KIs\Nova\speech\nova_voice_tests\nova_reference.wav"
OUTPUT_DIR = Path(r"D:\KIs\Nova\speech\nova_voice_tests")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

texts = {
     "01_neutral": """
    Guten Abend. Ich bin Nova, deine persönliche Assistentin.
    Die Analyse ist abgeschlossen und alle Systeme arbeiten innerhalb
    der normalen Parameter. Es wurden keine kritischen Probleme festgestellt.
    """
}

reference_path = Path(REFERENCE_AUDIO)

if not reference_path.exists():
    print("FEHLER: Referenzdatei wurde nicht gefunden!")
    print()
    print(f"Gesuchter Pfad:")
    print(reference_path)
    print()
    input("Enter zum Beenden...")
    raise SystemExit


print("Referenz gefunden:")
print(reference_path)
print()

print("Lade Chatterbox auf die GPU...")

model = ChatterboxMultilingualTTS.from_pretrained(
    device="cuda",
    t3_model="v3"
)

print("Chatterbox geladen.")
print()

for name, text in texts.items():

    print(f"Erzeuge: {name}")

    wav = model.generate(
        text,
        language_id="de",
        audio_prompt_path=REFERENCE_AUDIO,
        exaggeration=0.5,
        cfg_weight=0.5,
        temperature=0.8,
        repetition_penalty=2.0,
        min_p=0.05,
        top_p=1.0
)

    threshold = 0.01

    audio = wav.squeeze()

    indices = torch.where(
        torch.abs(audio) > threshold
    )[0]

    if len(indices) > 0:

        start = indices[0]
        end = indices[-1]

        padding = int(model.sr * 0.02)

        start = max(0, start - padding)
        end = min(len(audio), end + padding)

        wav = audio[start:end].unsqueeze(0)

    output_file = OUTPUT_DIR / f"nova_{name}.wav"

    audio = wav.detach().cpu().numpy()

    # Chatterbox liefert normalerweise [1, samples]
    if audio.ndim == 2 and audio.shape[0] == 1:
        audio = audio[0]

    # Mono explizit als [samples, 1]
    audio = audio.reshape(-1, 1)

    sf.write(
        str(output_file),
        audio,
        model.sr
    )

    print(f"Gespeichert: {output_file}")
    print()


print("========================================")
print("Alle Tests wurden erzeugt.")
print(f"Ordner: {OUTPUT_DIR}")
print("========================================")