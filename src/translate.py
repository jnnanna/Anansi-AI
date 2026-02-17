from __future__ import annotations

import os
from typing import Optional

_MOCK_TRANSLATIONS = {
    "bonjour": "salaam aleekum",
    "comment vas-tu": "nanga def",
    "je vais bien": "mangi fi rek",
}


def _mock_translate(text: str, target_lang: str) -> str:
    key = text.strip().lower()
    return _MOCK_TRANSLATIONS.get(key, f"[MOCK {target_lang}] {text}")


def translate_text(text: str, target_lang: str = "wo", gcloud_json_path: Optional[str] = None) -> str:
    """Translate text with GCP Translate API when configured, fallback to mock otherwise."""
    credentials_path = gcloud_json_path or os.getenv("GCLOUD_SERVICE_KEY_JSON", "").strip()
    if credentials_path:
        if credentials_path.startswith("{"):
            os.environ["GCLOUD_SERVICE_KEY_JSON_CONTENT"] = credentials_path
        else:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        try:
            from google.cloud import translate_v2 as translate  # type: ignore

            client = translate.Client()
            res = client.translate(text, target_language=target_lang)
            return res["translatedText"]
        except Exception:
            return _mock_translate(text, target_lang)
    return _mock_translate(text, target_lang)


if __name__ == "__main__":
    sample = "Bonjour"
    print(translate_text(sample, target_lang="wo"))
