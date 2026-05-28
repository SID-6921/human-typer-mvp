# human-typer-mvp

A small desktop tool that **types text for you as real keystrokes** into whatever
text field is focused. Useful when an app blocks paste (some web forms, exam
portals, remote-desktop windows, kiosk fields, accessibility scenarios, QA test
automation, etc.).

> Use it only on systems where you are allowed to automate input. Do **not**
> use it to bypass anti-cheat, exam-proctoring, or platform Terms of Service.

---

## What it does

- Reads text from a file, clipboard, or stdin.
- Types it character-by-character into the **currently focused** field.
- Adjustable **accuracy profile** (JSON): WPM, jitter, typo rate, auto-correct.
- Global **hotkeys** to start / pause / abort so you never lose control.
- Countdown before typing starts so you can click into the target field.

---

## Process — what to do, in order

1. **Install** (one time)
   ```powershell
   pip install -e .
   ```

2. **Pick or edit a profile** in `profiles/` (or use the default):
   - `profiles/natural.json`   — realistic human, ~60 WPM, small typos, auto-corrects
   - `profiles/fast.json`      — ~120 WPM, low typo rate
   - `profiles/robotic.json`   — constant speed, no typos
   - `profiles/careful.json`   — slow, zero typos (for fragile forms)

3. **Put the text you want typed** into `input.txt` (or pass `--text`, or pipe stdin).

4. **Run it:**
   ```powershell
   human-typer --file input.txt --profile profiles/natural.json --countdown 5
   ```

5. **Within the countdown**, click into the target text field (browser input,
   remote desktop, exam field, etc.) and leave it focused.

6. Typing begins automatically. Control it with hotkeys:
   - `F8`  — pause / resume
   - `Esc` — abort immediately

---

## CLI

```
human-typer [--file PATH | --text STRING | --stdin]
            [--profile PATH]
            [--countdown SECONDS]
            [--wpm N]            # override profile
            [--typo-rate 0..1]   # override profile
            [--dry-run]          # print what it would type, don't send keys
```

Examples:

```powershell
# Type contents of a file with the natural profile
human-typer --file input.txt --profile profiles/natural.json

# Type an inline string fast, no typos
human-typer --text "hello world" --profile profiles/fast.json

# Preview only — no real keystrokes sent
human-typer --file input.txt --profile profiles/natural.json --dry-run

# Pipe from clipboard (PowerShell)
Get-Clipboard | human-typer --stdin --profile profiles/natural.json
```

---

## Accuracy profile (JSON schema)

```json
{
  "wpm": 60,                 // target words per minute (5 chars = 1 word)
  "wpm_jitter": 0.25,        // 0..1 — random speed variation per keystroke
  "typo_rate": 0.02,         // 0..1 — probability of mistyping each char
  "auto_correct": true,      // if true, backspace and retype after a typo
  "correction_delay_ms": 180,// pause before correcting
  "thinking_pauses": true,   // longer pauses at punctuation / line breaks
  "newline_pause_ms": 350,
  "punct_pause_ms": 120,
  "shift_pause_ms": 25
}
```

You can pass `--wpm` or `--typo-rate` to override a profile field at runtime.

---

## Hotkeys

| Key | Action               |
|-----|----------------------|
| F8  | Pause / Resume       |
| Esc | Abort and exit       |

These work globally while the tool is running, so you can take back control
even if the wrong window is focused.

---

## Safety notes

- **Countdown is mandatory** (min 2s). If you don't focus a target field in
  time, the keystrokes will go wherever your cursor is — possibly your terminal.
- **Dry-run first** if you're unsure: `--dry-run` prints the planned keystrokes
  (including simulated typos and corrections) without touching the keyboard.
- The tool **never reads your screen** and **never sees the target app's
  contents**. It only sends keystrokes.

---

## Project layout

```
human-typer-mvp/
├── src/human_typer/
│   ├── __init__.py
│   ├── cli.py            # argparse + entry point
│   ├── engine.py         # typing engine (timing, typos, corrections)
│   ├── keyboard.py       # keystroke backend (pynput) + dry-run backend
│   ├── profile.py        # load/validate JSON profiles
│   └── hotkeys.py        # pause / abort hotkey listener
├── profiles/
│   ├── natural.json
│   ├── fast.json
│   ├── robotic.json
│   └── careful.json
├── tests/
│   └── test_engine.py
├── input.txt             # put text you want typed here
├── pyproject.toml
└── README.md
```

---

## Dev

```powershell
pip install -e ".[dev]"
pytest -q
```

---

## License

MIT
