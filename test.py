import torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

print("Lade Chatterbox auf die GPU...")

model=ChatterboxMultilingualTTS.from_pretrained(
    device="cuda"
)

text = """
Hey, ich bin Nova.
Schön, dass du da bist.
Wie kann ich dir helfen?
"""

print("Erzeuge Sprache...")

wav=model.generate(
    text,
    language_id="de"
)

ta.save(
    "nova_chatterbox.wav",
    wav,
    model.sr
)

print("Fertig: nova_chatterbox.wav")