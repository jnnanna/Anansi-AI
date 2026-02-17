from __future__ import annotations

import os
from pathlib import Path


def ensure_dir(path: str | Path) -> Path:
    """Create a directory if needed and return it as Path."""
    target = Path(path)
    target.mkdir(parents=True, exist_ok=True)
    return target


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def write_text_report(path: str | Path, title: str, lines: list[str]) -> Path:
    report_path = Path(path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    content = [f"# {title}", ""] + [f"- {line}" for line in lines]
    report_path.write_text("\n".join(content) + "\n", encoding="utf-8")
    return report_path
