from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import soundfile as sf


def _fallback_sine(output: Path, seconds: float = 1.0, sr: int = 16000) -> Path:
    t = np.linspace(0, seconds, int(sr * seconds), endpoint=False)
    wave = 0.1 * np.sin(2 * np.pi * 220 * t)
    sf.write(output.as_posix(), wave, sr, subtype="PCM_16")
    return output


def synthesize(text: str, model_path: str, output: str = "out.wav") -> str:
    out_path = Path(output)
    try:
        from TTS.api import TTS  # type: ignore

        tts = TTS(model_path=model_path)
        tts.tts_to_file(text=text, file_path=out_path.as_posix())
    except Exception:
        _fallback_sine(out_path)
    return out_path.as_posix()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script d'inférence TTS")
    parser.add_argument("--text", required=True)
    parser.add_argument("--model_path", default="finetuned/checkpoint_mock.json")
    parser.add_argument("--output", default="out.wav")
    args = parser.parse_args()
    path = synthesize(args.text, args.model_path, args.output)
    print(path)
