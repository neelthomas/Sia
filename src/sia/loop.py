from collections.abc import Callable
from typing import Protocol


class Backend(Protocol):
    def transcribe(self, wav: bytes) -> str: ...
    def reply(self, text: str) -> str: ...
    def synthesize(self, text: str) -> bytes: ...


EXIT_PHRASES = {"goodbye", "goodbye sia", "exit", "quit", "stop"}


def is_exit(text: str) -> bool:
    return text.lower().strip(" .!?,") in EXIT_PHRASES


def run_turn(
    backend: Backend,
    record: Callable[[], bytes | None],
    play: Callable[[bytes], None],
    log: Callable[[str], None] = print,
) -> bool:
    """One listen -> think -> speak cycle. Returns False when the user asks to stop."""
    wav = record()
    if wav is None:
        return True
    heard = backend.transcribe(wav)
    if not heard:
        return True
    log(f"you: {heard}")
    if is_exit(heard):
        play(backend.synthesize("Goodbye."))
        return False
    answer = backend.reply(heard)
    log(f"sia: {answer}")
    if answer:
        play(backend.synthesize(answer))
    return True
