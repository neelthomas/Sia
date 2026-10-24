from . import audio
from .config import Config
from .gemini import GeminiBackend
from .loop import run_turn


def main() -> None:
    backend = GeminiBackend(Config.from_env())
    print("Sia is listening. Say 'goodbye' or press Ctrl+C to quit.")
    try:
        while run_turn(backend, audio.record_utterance, audio.play_pcm):
            pass
    except KeyboardInterrupt:
        print()


if __name__ == "__main__":
    main()
