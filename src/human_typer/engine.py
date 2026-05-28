"""Typing engine: timing, typos, auto-correction."""
from __future__ import annotations

import random
import time
from dataclasses import dataclass
from typing import Callable

from .keyboard import KeyBackend
from .profile import Profile


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
    paused: bool = False
    aborted: bool = False


def _plausible_typo(ch: str) -> str:
    options = _ADJACENT.get(ch.lower())
    if not options:
        return ch
    wrong = random.choice(options)
    return wrong.upper() if ch.isupper() else wrong


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
    control = control or ControlState()
    rng = rng or random.Random()
    base = profile.char_delay_seconds()

    for ch in text:
        while control.paused and not control.aborted:
            sleep(0.05)
        if control.aborted:
            return

        if ch.isalpha() and rng.random() < profile.typo_rate:
            backend.type_char(_plausible_typo(ch))
            _delay(base, profile, rng, sleep)
            if profile.auto_correct:
                sleep(profile.correction_delay_ms / 1000.0)
                backend.backspace()
                _delay(base, profile, rng, sleep)

        backend.type_char(ch)

        if profile.thinking_pauses:
            if ch == "\n":
                sleep(profile.newline_pause_ms / 1000.0)
            elif _is_punct(ch):
                sleep(profile.punct_pause_ms / 1000.0)
            elif ch.isupper():
                sleep(profile.shift_pause_ms / 1000.0)

        _delay(base, profile, rng, sleep)


def _delay(base: float, profile: Profile, rng: random.Random, sleep: Callable[[float], None]) -> None:
    j = profile.wpm_jitter
    if j <= 0:
        sleep(base); return
    sleep(max(0.0, base * (1.0 + rng.uniform(-j, j))))
