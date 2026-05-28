"""Global hotkeys: F8 pause/resume, Esc abort."""
from __future__ import annotations

from .engine import ControlState


def start_listener(control: ControlState):
    from pynput import keyboard  # type: ignore

    def on_press(key):
        try:
            if key == keyboard.Key.esc:
                control.aborted = True
                return False
            if key == keyboard.Key.f8:
                control.paused = not control.paused
        except Exception:
            pass

    listener = keyboard.Listener(on_press=on_press)
    listener.daemon = True
    listener.start()
    return listener
