"""Keystroke backends: real (pynput) and dry-run (prints planned keys)."""
from __future__ import annotations

from typing import Protocol


class KeyBackend(Protocol):
    def type_char(self, ch: str) -> None: ...
    def backspace(self) -> None: ...


class DryRunBackend:
    """Collects/prints what would be typed without sending real keystrokes."""

    def __init__(self) -> None:
        self.buffer: list[str] = []

    def type_char(self, ch: str) -> None:
        self.buffer.append(ch)
        # Print without newline noise; flush each char.
        print(ch, end="", flush=True)

    def backspace(self) -> None:
        if self.buffer:
            self.buffer.pop()
        print("\b \b", end="", flush=True)


class PynputBackend:
    """Real keystroke backend using pynput."""

    def __init__(self) -> None:
        # Import here so dry-run users don't need pynput installed to import module.
        from pynput.keyboard import Controller, Key  # type: ignore

        self._Key = Key
        self._kb = Controller()

    def type_char(self, ch: str) -> None:
        if ch == "\n":
            self._kb.press(self._Key.enter)
            self._kb.release(self._Key.enter)
        elif ch == "\t":
            self._kb.press(self._Key.tab)
            self._kb.release(self._Key.tab)
        else:
            self._kb.type(ch)

    def backspace(self) -> None:
        self._kb.press(self._Key.backspace)
        self._kb.release(self._Key.backspace)
