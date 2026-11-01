# Nova – lokale KI-Sprachassistentin

Nova ist eine persönliche KI-Assistentin, die komplett auf dem eigenen Windows-PC läuft. Du sprichst mit ihr auf Deutsch, sie entscheidet selbst, ob sie ein Tool braucht (zum Beispiel ein Programm öffnen), und antwortet mit geklonter Stimme.

## Features

- Spracheingabe mit faster-whisper, Sprachausgabe mit Chatterbox TTS
- Lokales LLM über Ollama (`qwen3:4b-instruct`) mit nativem Tool Calling, ohne feste Trigger im Code
- Tools laden sich automatisch: neue Datei in `tools/` anlegen, fertig
- Gedächtnis in SQLite („Merk dir, dass …")
- GUI mit Audio-Visualizer (pygame)

## Voraussetzungen

- Windows, Python 3.13
- NVIDIA-GPU mit CUDA (getestet: RTX 3060, 12 GB)
- [Ollama](https://ollama.com)
- Mikrofon und eine eigene Referenzaufnahme für die Stimme

## Installation

```powershell
python -m venv venv
venv\Scripts\activate
```

1. PyTorch mit CUDA installieren ([pytorch.org](https://pytorch.org))
2. Pakete installieren:
   ```powershell
   pip install ollama SpeechRecognition PyAudio faster-whisper chatterbox-tts pygame soundfile numpy sentence-transformers
   ```
3. Modell laden: `ollama pull qwen3:4b-instruct`
4. Pfad zur Referenzstimme in `speech/speech.py` anpassen (`REFERENCE_AUDIO`)
5. Einstellungen in `config.py` prüfen (Modell, Sprache, Datenbank)

## Starten

```powershell
python main.py
```

Beispiele: „Öffne Spotify", „Wie spät ist es?", „Merk dir, dass ich Volleyball mag". Mit „Stopp" beendest du Nova.

## Eigenes Tool hinzufügen

```python
# tools/beispiel.py
from tools.tool_registry import register_tool

def get_weather(city):
    """Liefert das Wetter für eine Stadt.

    Args:
        city: Name der Stadt, z.B. "Berlin".
    """
    return f"In {city} ist es sonnig."  # Platzhalter

register_tool("get_weather", "Liefert das Wetter für eine Stadt.", get_weather)
```

## Hinweis zur Stimme

Verwende für die Stimmklonung nur Aufnahmen von Personen, die zugestimmt haben (am besten deine eigene Stimme).
