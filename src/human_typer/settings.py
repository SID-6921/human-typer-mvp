"""Persistent user settings stored in %APPDATA%\\human-typer\\config.json."""
from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path


def _config_dir() -> Path:
    base = os.environ.get("APPDATA") or str(Path.home() / ".config")
    p = Path(base) / "human-typer"
    p.mkdir(parents=True, exist_ok=True)
    return p


def _config_path() -> Path:
    return _config_dir() / "config.json"


@dataclass
class Settings:
    profile: str = "natural"
    wpm: int = 60
    typo_percent: float = 2.5
    countdown: int = 10
    window_geometry: str = ""

    @classmethod
    def load(cls) -> "Settings":
        path = _config_path()
        if not path.exists():
            return cls()
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return cls()
        allowed = {f for f in cls().__dict__}
        clean = {k: v for k, v in data.items() if k in allowed}
        try:
            return cls(**clean)
        except TypeError:
            return cls()

    def save(self) -> None:
        try:
            _config_path().write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")
        except Exception:
            pass
