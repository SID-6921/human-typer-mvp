"""Accuracy profile loading and validation."""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path


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
    def load(cls, path: str | Path) -> "Profile":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict) -> "Profile":
        allowed = {f for f in cls().__dict__}
        clean = {k: v for k, v in data.items() if k in allowed}
        p = cls(**clean)
        p.validate()
        return p

    def validate(self) -> None:
        if not (1 <= self.wpm <= 1000):
            raise ValueError("wpm must be between 1 and 1000")
        if not (0.0 <= self.wpm_jitter <= 1.0):
            raise ValueError("wpm_jitter must be between 0 and 1")
        if not (0.0 <= self.typo_rate <= 1.0):
            raise ValueError("typo_rate must be between 0 and 1")

    def char_delay_seconds(self) -> float:
        # 5 chars per "word"; convert wpm to seconds per char.
        cps = (self.wpm * 5.0) / 60.0
        return 1.0 / max(cps, 0.001)

    def to_dict(self) -> dict:
        return asdict(self)
