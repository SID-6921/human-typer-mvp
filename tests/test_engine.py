"""Tests for the typing engine using the dry-run backend and fake sleep."""
from __future__ import annotations

import random

from human_typer.engine import ControlState, type_text
from human_typer.keyboard import DryRunBackend
from human_typer.profile import Profile


class _NoSleep:
    def __init__(self) -> None:
        self.total = 0.0

    def __call__(self, s: float) -> None:
        self.total += s


def test_robotic_profile_types_text_exactly(capsys):
    profile = Profile(wpm=600, wpm_jitter=0.0, typo_rate=0.0,
                      auto_correct=False, thinking_pauses=False)
    backend = DryRunBackend()
    type_text("hello", backend, profile, sleep=_NoSleep(), rng=random.Random(0))
    assert "".join(backend.buffer) == "hello"


def test_typo_with_autocorrect_yields_final_text():
    profile = Profile(wpm=600, wpm_jitter=0.0, typo_rate=1.0,
                      auto_correct=True, thinking_pauses=False,
                      correction_delay_ms=0)
    backend = DryRunBackend()
    type_text("abc", backend, profile, sleep=_NoSleep(), rng=random.Random(1))
    # After every typo is corrected, the final buffer must equal the input.
    assert "".join(backend.buffer) == "abc"


def test_abort_stops_typing_midway():
    profile = Profile(wpm=600, wpm_jitter=0.0, typo_rate=0.0,
                      auto_correct=False, thinking_pauses=False)
    backend = DryRunBackend()
    ctl = ControlState(aborted=True)
    type_text("hello world", backend, profile, control=ctl, sleep=_NoSleep())
    assert backend.buffer == []


def test_profile_load_and_validate(tmp_path):
    p = tmp_path / "prof.json"
    p.write_text('{"wpm": 80, "typo_rate": 0.01}', encoding="utf-8")
    prof = Profile.load(p)
    assert prof.wpm == 80
    assert prof.typo_rate == 0.01
