import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    api_key: str
    chat_model: str = "gemini-2.5-flash"
    stt_model: str = "gemini-2.5-flash"
    tts_model: str = "gemini-2.5-flash-preview-tts"
    voice: str = "Kore"
    system_prompt: str = (
        "You are Sia, a voice assistant. Your replies are spoken aloud, so keep them short, "
        "conversational, and free of markdown, lists, or emoji."
    )

    @classmethod
    def from_env(cls) -> "Config":
        key = os.environ.get("GEMINI_API_KEY")
        if not key:
            raise SystemExit("GEMINI_API_KEY is not set (see .env.example).")
        return cls(
            api_key=key,
            chat_model=os.environ.get("SIA_CHAT_MODEL", cls.chat_model),
            stt_model=os.environ.get("SIA_STT_MODEL", cls.stt_model),
            tts_model=os.environ.get("SIA_TTS_MODEL", cls.tts_model),
            voice=os.environ.get("SIA_VOICE", cls.voice),
        )
