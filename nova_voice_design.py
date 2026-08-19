import torch
import soundfile as sf

from qwen_tts import Qwen3TTSModel


print("Lade Qwen3-TTS...")

model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
    device_map="cuda",
    dtype=torch.bfloat16,
    attn_implementation="sdpa",
)

texts = {

    "01_neutral": """
Guten Abend. Ich bin Nova, deine persönliche Assistentin.
Die Analyse ist abgeschlossen und alle Systeme arbeiten innerhalb
der normalen Parameter. Es wurden keine kritischen Probleme festgestellt.
""",

   "02_ironisch": """
Ich habe die Situation überprüft und kann dich beruhigen.
Du hast tatsächlich erneut die falsche Schaltfläche ausgewählt.
Keine Sorge, ich werde versuchen, deine Entscheidung nicht persönlich zu nehmen.
""",

    "03_trocken": """
Natürlich kann ich das für dich erledigen.
Schließlich wäre es ausgesprochen unpraktisch,
wenn eine hochentwickelte künstliche Intelligenz nicht dazu in der Lage wäre.
""",

    "04_ernst": """
Ich habe die aktuellen Systemdaten analysiert.
Es wurde eine ungewöhnliche Aktivität festgestellt.
Ich empfehle, den Vorgang vorerst nicht fortzusetzen,
bis die Ursache eindeutig identifiziert wurde.
""",

    "05_freundlich": """
Das klingt nach einem guten Plan.
Ich kümmere mich darum und bereite die notwendigen Informationen vor.
Du kannst dich in der Zwischenzeit um andere Dinge kümmern.
"""
}



voices = {

    "04A_1E": """
Female native German AI voice, approximately 30 to 40 years old.

A highly advanced futuristic personal artificial intelligence
with the sophisticated presence of a digital personal assistant.

The speaker is a native German woman speaking neutral Standard German.

Use authentic native German pronunciation and natural German prosody.
Use standard German pronunciation as heard in professional German speech.
German vowel sounds, consonants, word stress and sentence melody
must sound naturally German.

No regional dialect.
No foreign accent.
No English-influenced pronunciation.
No American pronunciation.
No British pronunciation.

Calm, intelligent, confident and composed.
Medium-low female pitch.
Smooth, refined and moderately warm vocal timbre.
Slightly cool and technological, but with subtle warmth.

The voice should clearly sound like an advanced artificial intelligence,
not like an ordinary human woman.

Very clear and precise articulation.
Controlled, restrained and conversational delivery.

Normal informational sentences should have mostly even pitch
and restrained emphasis.
Do not exaggerate individual words.
Do not sound like a narrator or presenter.

She is polite, attentive, highly capable and observant.
She speaks with quiet confidence and subtle authority.

Her personality is intelligent and composed,
with a sophisticated and understated sense of humor.

She can express subtle dry humor, irony and sarcasm when the
context naturally calls for it.

Sarcasm should be dry, intelligent and restrained.
Never exaggerated or theatrical.

When the text is neutral or informational,
use calm and understated delivery.

When the meaning is humorous, ironic or sarcastic,
subtle changes in timing, intonation and emphasis may communicate
the humor.

When the meaning is serious or urgent,
slightly stronger emphasis may be used.

The emotional expression must follow the meaning of the text.

Moderate speaking speed.
Natural German pauses.
Mostly even pacing.

The overall impression should be:
a sophisticated female German AI assistant with the intelligence,
confidence, subtle wit and presence of a futuristic digital butler.

Futuristic without sounding like science fiction.
Artificial without sounding robotic.
Warm without sounding overly human.

Never use a foreign accent.
Never use English pronunciation.
Never over-emphasize normal sentences.
Never constantly expressive.
Never constantly sarcastic.
Never cold.
Never robotic.
Never overly human.
Never bubbly.
Never theatrical.
"""
}


for name, text in texts.items():

    print(f"Erzeuge: {name}")

    wavs, sr = model.generate_voice_design(
        text=text,
        language="German",
        instruct=voices["04A_1E"],
    )

    filename = f"nova_{name}.wav"

    sf.write(
        filename,
        wavs[0],
        sr
    )

    print(f"Gespeichert: {filename}")

print("\nAlle Stimmen wurden erzeugt.")