from google import genai
from google.genai import types

from .config import Config


class GeminiBackend:
    """Speech-to-text, chat, and text-to-speech, all through one Gemini API key."""

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.client = genai.Client(api_key=cfg.api_key)
        self.chat = self.client.chats.create(
            model=cfg.chat_model,
            config=types.GenerateContentConfig(system_instruction=cfg.system_prompt),
        )

    def transcribe(self, wav: bytes) -> str:
        resp = self.client.models.generate_content(
            model=self.cfg.stt_model,
            contents=[
                ("Transcribe this audio verbatim. Reply with only the transcript, "
                 "or an empty string if there is no intelligible speech."),
                types.Part.from_bytes(data=wav, mime_type="audio/wav"),
            ],
        )
        return (resp.text or "").strip()

    def reply(self, text: str) -> str:
        return (self.chat.send_message(text).text or "").strip()

    def synthesize(self, text: str) -> bytes:
        resp = self.client.models.generate_content(
            model=self.cfg.tts_model,
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=self.cfg.voice)
                    )
                ),
            ),
        )
        return resp.candidates[0].content.parts[0].inline_data.data
