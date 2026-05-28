"""Command-line interface (power-user)."""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from .engine import ControlState, type_text
from .keyboard import DryRunBackend, PynputBackend
from .profile import Profile


def _read_input(args: argparse.Namespace) -> str:
    if args.text is not None:
        return args.text
    if args.file:
        return Path(args.file).read_text(encoding="utf-8")
    if args.stdin:
        return sys.stdin.read()
    default = Path("input.txt")
    if default.exists():
        return default.read_text(encoding="utf-8")
    raise SystemExit("No input. Use --file, --text, --stdin, or create input.txt.")


def _load_profile(args: argparse.Namespace) -> Profile:
    profile = Profile.load(args.profile) if args.profile else Profile()
    if args.wpm is not None:
        profile.wpm = args.wpm
    if args.typo_rate is not None:
        profile.typo_rate = args.typo_rate
    profile.validate()
    return profile


def _countdown(seconds: int) -> None:
    seconds = max(2, seconds)
    print(f"Focus target field. Typing starts in {seconds}s (F8 pause, Esc abort)...", flush=True)
    for i in range(seconds, 0, -1):
        print(f"  {i}...", flush=True)
        time.sleep(1)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="human-typer",
                                description="Type text as real keystrokes into the focused window.")
    src = p.add_mutually_exclusive_group()
    src.add_argument("--file", help="Path to a text file.")
    src.add_argument("--text", help="Literal text to type.")
    src.add_argument("--stdin", action="store_true", help="Read text from stdin.")
    p.add_argument("--profile", help="Profile name (natural/fast/robotic/careful) or path to JSON.")
    p.add_argument("--countdown", type=int, default=10, help="Seconds before typing starts (min 2).")
    p.add_argument("--wpm", type=float, help="Override profile WPM.")
    p.add_argument("--typo-rate", type=float, dest="typo_rate", help="Override profile typo rate (0..1).")
    p.add_argument("--dry-run", action="store_true", help="Print planned keystrokes; do not send keys.")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    text = _read_input(args)
    profile = _load_profile(args)
    control = ControlState()

    if args.dry_run:
        backend = DryRunBackend(on_char=lambda c: print(c, end="" if c != "\b" else "\b \b", flush=True))
        print("[dry-run] no real keystrokes will be sent.\n", flush=True)
        type_text(text, backend, profile, control=control)
        print("\n[dry-run] done.", flush=True)
        return 0

    backend = PynputBackend()
    from .hotkeys import start_listener
    start_listener(control)
    _countdown(args.countdown)
    type_text(text, backend, profile, control=control)
    print("\nAborted." if control.aborted else "\nDone.", flush=True)
    return 130 if control.aborted else 0


if __name__ == "__main__":
    raise SystemExit(main())
