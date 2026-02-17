from __future__ import annotations

import argparse
import csv
import shutil
import sys
from pathlib import Path

from utils import ensure_dir


def normalize_wav(source: Path, destination: Path, sample_rate: int = 16000) -> None:
    import librosa
    import soundfile as sf

    audio, _ = librosa.load(source.as_posix(), sr=sample_rate, mono=True)
    sf.write(destination.as_posix(), audio, sample_rate, subtype="PCM_16")


def prepare_dataset(input_dir: str, output_dir: str, metadata_name: str = "metadata.csv") -> Path:
    in_root = Path(input_dir)
    out_root = ensure_dir(output_dir)
    out_audio = ensure_dir(out_root / "audios")

    metadata_in = in_root / metadata_name
    metadata_out = out_root / metadata_name

    if not metadata_in.exists():
        metadata_out.write_text("", encoding="utf-8")
        return metadata_out

    kept_rows: list[tuple[str, str]] = []
    with metadata_in.open("r", encoding="utf-8") as handle:
        reader = csv.reader(handle, delimiter="|")
        for row in reader:
            if len(row) < 2:
                continue
            wav_name, text = row[0].strip(), row[1].strip()
            src = in_root / "audios" / wav_name
            dst = out_audio / wav_name
            if not src.exists() or not text:
                continue
            try:
                normalize_wav(src, dst)
            except (ImportError, OSError, ValueError) as exc:
                print(f"[prepare_dataset.py] normalisation impossible pour {wav_name}: {exc}", file=sys.stderr)
                shutil.copy2(src, dst)
            kept_rows.append((wav_name, text))

    with metadata_out.open("w", encoding="utf-8") as handle:
        for wav_name, text in kept_rows:
            handle.write(f"{wav_name}|{text}\n")

    return metadata_out


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare TTS dataset to 16kHz mono + metadata")
    parser.add_argument("--input_dir", required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--metadata", default="metadata.csv")
    args = parser.parse_args()
    result = prepare_dataset(args.input_dir, args.output_dir, args.metadata)
    print(f"Dataset prêt: {result}")


if __name__ == "__main__":
    main()
