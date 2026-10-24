# Sia

A custom voice assistant (an "Alexa" of your own) powered by Gemini.

Pipeline: microphone -> silence-based endpointing -> Gemini speech-to-text ->
Gemini chat (with conversation memory) -> Gemini text-to-speech -> speaker.

## Setup (no Claude needed to run it)

1. Get a free Gemini API key at https://aistudio.google.com (Get API key).
2. Install Python 3.11+ from https://python.org.
3. In this folder, create a file named `.env` containing one line: `GEMINI_API_KEY=your-key`
4. Run:

```
python -m venv .venv
.venv\Scripts\activate          (Windows)   |   source .venv/bin/activate   (Mac/Linux)
pip install -e .
sia
```

Speak, pause, and Sia answers. Say "goodbye" or press Ctrl+C to quit.
Needs a machine with a microphone and speakers (not a cloud container).

### Using a Bluetooth speaker

Pair the speaker with your computer and choose it as the sound output. Sia plays
through the default output device, so no code change is needed. Sia listens through
the computer's microphone.

## Layout

- `src/sia/audio.py` - recording, endpointing, playback
- `src/sia/gemini.py` - Gemini STT, chat, TTS
- `src/sia/loop.py` - one listen/think/speak turn (backend is injectable, so it is testable)
- `tests/` - `pytest`

## Next

Wake word, tool calling (calendar, smart home, data queries), streaming TTS, barge-in.
