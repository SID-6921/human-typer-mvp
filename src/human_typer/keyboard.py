"""Keystroke backends."""
from __future__ import annotations

from typing import Callable, Protocol


class KeyBackend(Protocol):
    def type_char(self, ch: str) -> None: ...
    def backspace(self) -> None: ...


class DryRunBackend:
    """Buffers planned keystrokes; optionally streams them to a callback."""

    def __init__(self, on_char: Callable[[str], None] | None = None) -> None:
        self.buffer: list[str] = []
        self._on_char = on_char

    def type_char(self, ch: str) -> None:
        self.buffer.append(ch)
        if self._on_char:
            self._on_char(ch)

    def backspace(self) -> None:
        if self.buffer:
            self.buffer.pop()
        if self._on_char:
            self._on_char("\b")


class PynputBackend:
    def __init__(self) -> None:
        from pynput.keyboard import Controller, Key  # type: ignore
        self._Key = Key
        self._kb = Controller()

    def type_char(self, ch: str) -> None:
        if ch == "\n":
            self._kb.press(self._Key.enter); self._kb.release(self._Key.enter)
        elif ch == "\t":
            self._kb.press(self._Key.tab); self._kb.release(self._Key.tab)
        else:
            self._kb.type(ch)

    def backspace(self) -> None:
        self._kb.press(self._Key.backspace); self._kb.release(self._Key.backspace)
