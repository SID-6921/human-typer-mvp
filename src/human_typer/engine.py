"""Typing engine: timing, typos, auto-correction."""
from __future__ import annotations

import random
import time
from dataclasses import dataclass
from typing import Callable

from .keyboard import KeyBackend
from .profile import Profile


# Adjacency map for plausible "fat-finger" typos on a QWERTY layout.
_ADJACENT = {
    "a": "qwsz", "b": "vghn", "c": "xdfv", "d": "serfcx", "e": "wsdr",
    "f": "drtgvc", "g": "ftyhbv", "h": "gyujnb", "i": "ujko", "j": "huikmn",
    "k": "jiolm", "l": "kop", "m": "njk", "n": "bhjm", "o": "iklp",
    "p": "ol", "q": "wa", "r": "edft", "s": "awedxz", "t": "rfgy",
    "u": "yhji", "v": "cfgb", "w": "qase", "x": "zsdc", "y": "tghu",
    "z": "asx",
}


@dataclass
class ControlState:
    """Shared flags toggled by the hotkey listener."""
    paused: bool = False
    aborted: bool = False


def _plausible_typo(ch: str) -> str:
    lower = ch.lower()
    options = _ADJACENT.get(lower)
    if not options:
        return ch
    mistake = random.choice(options)
    return mistake.upper() if ch.isupper() else mistake


def _is_punct(ch: str) -> bool:
    return ch in ",.;:!?)"


def type_text(
    text: str,
    backend: KeyBackend,
    profile: Profile,
    control: ControlState | None = None,
    sleep: Callable[[float], None] = time.sleep,
    rng: random.Random | None = None,
) -> None:
    """Type `text` through `backend` using `profile`.

    Honors pause/abort via `control`. `sleep` and `rng` are injectable for tests.
    """
    control = control or ControlState()
    rng = rng or random.Random()
    base_delay = profile.char_delay_seconds()

    for ch in text:
        # Handle control flags between every char.
        while control.paused and not control.aborted:
            sleep(0.05)
        if control.aborted:
            return

        # Maybe inject a typo (only for letters).
        if ch.isalpha() and rng.random() < profile.typo_rate:
            wrong = _plausible_typo(ch)
            backend.type_char(wrong)
            _delay(base_delay, profile, rng, sleep)

            if profile.auto_correct:
                sleep(profile.correction_delay_ms / 1000.0)
                backend.backspace()
                _delay(base_delay, profile, rng, sleep)

        # Type the actual character.
        backend.type_char(ch)

        # Extra "thinking" pauses.
        if profile.thinking_pauses:
            if ch == "\n":
                sleep(profile.newline_pause_ms / 1000.0)
            elif _is_punct(ch):
                sleep(profile.punct_pause_ms / 1000.0)
            elif ch.isupper():
                sleep(profile.shift_pause_ms / 1000.0)

        _delay(base_delay, profile, rng, sleep)


def _delay(base: float, profile: Profile, rng: random.Random, sleep: Callable[[float], None]) -> None:
    jitter = profile.wpm_jitter
    if jitter <= 0:
        sleep(base)
        return
    factor = 1.0 + rng.uniform(-jitter, jitter)
    sleep(max(0.0, base * factor))
