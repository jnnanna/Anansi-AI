from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, SRC.as_posix())

from prepare_dataset import prepare_dataset
from synthesize import synthesize


def test_prepare_dataset_handles_missing_metadata(tmp_path):
    input_dir = tmp_path / "in"
    output_dir = tmp_path / "out"
    input_dir.mkdir()

    metadata_path = prepare_dataset(input_dir.as_posix(), output_dir.as_posix())

    assert metadata_path.exists()
    assert metadata_path.read_text(encoding="utf-8") == ""


def test_synthesize_creates_wav_in_fallback(tmp_path):
    out_file = tmp_path / "demo.wav"
    output = synthesize("Nanga def", "missing-model", out_file.as_posix())
    assert Path(output).exists()
    assert Path(output).stat().st_size > 0
