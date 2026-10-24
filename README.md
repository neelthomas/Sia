# Sia

A custom voice assistant (an "Alexa" of your own) powered by Gemini.

Pipeline: microphone -> silence-based endpointing -> Gemini speech-to-text ->
Gemini chat (with conversation memory) -> Gemini text-to-speech -> speaker.

## Run

```
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # add GEMINI_API_KEY, then: export $(cat .env | xargs)
sia
```

Speak, pause, and Sia answers. Say "goodbye" or press Ctrl+C to quit.
Needs a machine with a microphone and speakers (not a cloud container).

## Layout

- `src/sia/audio.py` - recording, endpointing, playback
- `src/sia/gemini.py` - Gemini STT, chat, TTS
- `src/sia/loop.py` - one listen/think/speak turn (backend is injectable, so it is testable)
- `tests/` - `pytest`

## Next

Wake word, tool calling (calendar, smart home, data queries), streaming TTS, barge-in.
