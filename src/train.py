from __future__ import annotations

import argparse
import json
from pathlib import Path

from utils import ensure_dir


def run_train(output_dir: str, epochs: int = 1, backend: str = "xtts") -> Path:
    target = ensure_dir(output_dir)
    checkpoint = target / "checkpoint_mock.json"
    checkpoint.write_text(
        json.dumps({"status": "ok", "backend": backend, "epochs": epochs}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return checkpoint


def main() -> None:
    parser = argparse.ArgumentParser(description="Wrapper de fine-tuning (prototype)")
    parser.add_argument("--dataset_dir", required=True)
    parser.add_argument("--output_dir", default="finetuned")
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--backend", choices=["xtts", "speecht5"], default="xtts")
    args = parser.parse_args()

    checkpoint = run_train(args.output_dir, args.epochs, args.backend)
    print(f"Entraînement prototype terminé. Checkpoint: {checkpoint}")


if __name__ == "__main__":
    main()
