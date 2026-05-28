"""Engine tests using the dry-run backend."""
from __future__ import annotations

import random

from human_typer.engine import ControlState, type_text
from human_typer.keyboard import DryRunBackend
from human_typer.profile import Profile


class _NoSleep:
    def __init__(self): self.total = 0.0
    def __call__(self, s): self.total += s


def test_clean_typing_matches_text():
    p = Profile(wpm=600, wpm_jitter=0, typo_rate=0, auto_correct=False, thinking_pauses=False)
    b = DryRunBackend()
    type_text("hello", b, p, sleep=_NoSleep(), rng=random.Random(0))
    assert "".join(b.buffer) == "hello"


def test_typo_with_autocorrect_yields_final_text():
    p = Profile(wpm=600, wpm_jitter=0, typo_rate=1.0, auto_correct=True,
                thinking_pauses=False, correction_delay_ms=0)
    b = DryRunBackend()
    type_text("abc", b, p, sleep=_NoSleep(), rng=random.Random(1))
    assert "".join(b.buffer) == "abc"


def test_abort_stops_typing():
    p = Profile(wpm=600, wpm_jitter=0, typo_rate=0, auto_correct=False, thinking_pauses=False)
    b = DryRunBackend()
    type_text("hello", b, p, control=ControlState(aborted=True), sleep=_NoSleep())
    assert b.buffer == []


def test_bundled_profile_loads():
    p = Profile.load("natural")
    assert p.wpm > 0
