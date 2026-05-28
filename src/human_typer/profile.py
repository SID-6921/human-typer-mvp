"""Accuracy profile: dataclass + JSON loader + bundled-profile resolver."""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from importlib import resources
from pathlib import Path


BUNDLED = {"natural", "fast", "robotic", "careful"}


@dataclass
class Profile:
    wpm: float = 60.0
    wpm_jitter: float = 0.25
    typo_rate: float = 0.02
    auto_correct: bool = True
    correction_delay_ms: int = 180
    thinking_pauses: bool = True
    newline_pause_ms: int = 350
    punct_pause_ms: int = 120
    shift_pause_ms: int = 25

    @classmethod
    def from_dict(cls, data: dict) -> "Profile":
        allowed = {f for f in cls().__dict__}
        clean = {k: v for k, v in data.items() if k in allowed}
        p = cls(**clean)
        p.validate()
        return p

    @classmethod
    def load(cls, name_or_path: str) -> "Profile":
        """Accepts a bundled name ('natural') or a path to a JSON file."""
        if name_or_path in BUNDLED:
            text = (resources.files("human_typer.profiles") / f"{name_or_path}.json").read_text(encoding="utf-8")
        else:
            text = Path(name_or_path).read_text(encoding="utf-8")
        return cls.from_dict(json.loads(text))

    def validate(self) -> None:
        if not (1 <= self.wpm <= 1000):
            raise ValueError("wpm must be 1..1000")
        if not (0.0 <= self.wpm_jitter <= 1.0):
            raise ValueError("wpm_jitter must be 0..1")
        if not (0.0 <= self.typo_rate <= 1.0):
            raise ValueError("typo_rate must be 0..1")

    def char_delay_seconds(self) -> float:
        cps = (self.wpm * 5.0) / 60.0
        return 1.0 / max(cps, 0.001)

    def to_dict(self) -> dict:
        return asdict(self)
