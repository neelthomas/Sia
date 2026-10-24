import numpy as np

from sia.audio import BLOCK_SECONDS, Endpointer, to_wav
from sia.loop import is_exit, run_turn

LOUD = np.full(1600, 3000, dtype=np.int16)
QUIET = np.zeros(1600, dtype=np.int16)


def test_endpointer_waits_for_speech_then_silence():
    ep = Endpointer(silence_seconds=0.3)
    assert not any(ep.feed(QUIET) for _ in range(20))
    assert not ep.feed(LOUD)
    n = round(0.3 / BLOCK_SECONDS)
    results = [ep.feed(QUIET) for _ in range(n)]
    assert results[-1] and not any(results[:-1])


def test_endpointer_max_length():
    ep = Endpointer(max_seconds=0.5)
    assert any(ep.feed(QUIET) for _ in range(5))


def test_to_wav_header():
    assert to_wav(b"\x00\x00" * 10)[:4] == b"RIFF"


class FakeBackend:
    def __init__(self, heard):
        self.heard, self.spoken = heard, []

    def transcribe(self, wav):
        return self.heard

    def reply(self, text):
        return f"echo {text}"

    def synthesize(self, text):
        self.spoken.append(text)
        return text.encode()


def test_turn_speaks_reply():
    b, played = FakeBackend("hello"), []
    assert run_turn(b, lambda: b"wav", played.append, log=lambda s: None)
    assert played == [b"echo hello"]


def test_turn_exit_and_silence():
    b = FakeBackend("Goodbye.")
    assert not run_turn(b, lambda: b"wav", lambda p: None, log=lambda s: None)
    assert is_exit("quit")
    assert run_turn(FakeBackend(""), lambda: None, lambda p: None, log=lambda s: None)


def test_load_dotenv(tmp_path, monkeypatch):
    from sia.config import load_dotenv

    monkeypatch.delenv("SIA_TEST_KEY", raising=False)
    env = tmp_path / ".env"
    env.write_text("# c\nSIA_TEST_KEY='abc'\n")
    load_dotenv(env)
    import os
    assert os.environ["SIA_TEST_KEY"] == "abc"
    monkeypatch.delenv("SIA_TEST_KEY")
