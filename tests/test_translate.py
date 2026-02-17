from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, SRC.as_posix())

from translate import translate_text


def test_translate_fallback_returns_mock_marker():
    result = translate_text("Texte libre", target_lang="wo")
    assert result.startswith("[MOCK wo]")


def test_translate_known_mock_dictionary():
    result = translate_text("Bonjour", target_lang="wo")
    assert "salaam" in result.lower()
