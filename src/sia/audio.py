import io
import wave

import numpy as np

CAPTURE_RATE = 16_000
PLAYBACK_RATE = 24_000  # Gemini TTS returns 24 kHz mono 16-bit PCM
BLOCK_SECONDS = 0.1


def rms(block: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(block.astype(np.float64)))))


class Endpointer:
    """Decides when an utterance has finished: speech was heard, then enough silence."""

    def __init__(self, threshold: float = 500.0, silence_seconds: float = 1.0,
                 max_seconds: float = 20.0):
        self.threshold = threshold
        self.silence_blocks = round(silence_seconds / BLOCK_SECONDS)
        self.max_blocks = round(max_seconds / BLOCK_SECONDS)
        self.heard_speech = False
        self._silent = 0
        self._total = 0

    def feed(self, block: np.ndarray) -> bool:
        """Returns True once the utterance is complete."""
        self._total += 1
        if rms(block) >= self.threshold:
            self.heard_speech = True
            self._silent = 0
        else:
            self._silent += 1
        if self._total >= self.max_blocks:
            return True
        return self.heard_speech and self._silent >= self.silence_blocks


def to_wav(pcm: bytes, rate: int = CAPTURE_RATE) -> bytes:
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(pcm)
    return buf.getvalue()


def record_utterance(endpointer: Endpointer | None = None) -> bytes | None:
    """Blocks until the user speaks and stops; returns WAV bytes, or None if nothing was said."""
    import sounddevice as sd

    ep = endpointer or Endpointer()
    chunks: list[np.ndarray] = []
    block = int(CAPTURE_RATE * BLOCK_SECONDS)
    with sd.InputStream(samplerate=CAPTURE_RATE, channels=1, dtype="int16",
                        blocksize=block) as stream:
        while True:
            data, _ = stream.read(block)
            data = data[:, 0]
            if ep.heard_speech or rms(data) >= ep.threshold:
                chunks.append(data)
            if ep.feed(data):
                break
    if not ep.heard_speech:
        return None
    return to_wav(np.concatenate(chunks).tobytes())


def play_pcm(pcm: bytes, rate: int = PLAYBACK_RATE) -> None:
    import sounddevice as sd

    sd.play(np.frombuffer(pcm, dtype=np.int16), samplerate=rate)
    sd.wait()
