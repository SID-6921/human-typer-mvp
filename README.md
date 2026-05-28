# human-typer

**Type any text into any focused window — like a real human typing.**
For when paste (`Ctrl+V`) is blocked, disabled, or impossible.

A tiny Windows app. No CLI required. No admin rights. No Git. Runs on a
locked-down office laptop.

---

## TL;DR

> **The 30-second version:**
> 1. Download **`human-typer.exe`** from the [latest release](https://github.com/SID-6921/human-typer-mvp/releases/latest).
> 2. Double-click it. A small window opens.
> 3. Paste your text → click **Start** → click into Word / your form within 10 seconds.
> 4. Press **Esc** any time to stop.
>
> That's it.

---

## Why this exists

Sometimes you have text on one side and a text box on the other, and the gap
between them is artificially closed:

- A web form that disables paste.
- A remote-desktop or Citrix session with no shared clipboard.
- A kiosk-style app that swallows `Ctrl+V`.
- A screen recording where you want typing to *look* like typing, not like a
  paste.
- An accessibility need to feed long passages into apps that don't support
  assistive input well.

`human-typer` solves this the boring, reliable way: it sends real keystrokes,
one at a time, into whatever window has focus — with adjustable speed and
optional realistic typos.

> Use it only where you're allowed to automate keyboard input.
> Do **not** use it to defeat anti-cheat, exam-proctoring, or platform Terms
> of Service.

---

## Install — pick whichever your laptop allows

There are three install paths, ordered from easiest to most restricted
environment. They all produce the same app.

### Option 1 — Single `.exe` (zero install)

Best for: **most people**, especially office laptops.

1. Open <https://github.com/SID-6921/human-typer-mvp/releases/latest>.
2. Under **Assets**, download **`human-typer.exe`**.
3. Double-click it. Done.

No Python, no folder, no setup. To uninstall: delete the file.

> On first launch Windows SmartScreen may warn that the publisher is unknown.
> Click *More info → Run anyway* if you trust the source.

### Option 2 — From source (needs Python 3.10+, has internet)

Best for: **developers**, or laptops where `.exe` downloads are blocked but
Python is available.

1. **Install Python** from the Microsoft Store (search *"Python 3.12"*).
   No admin password needed. If the Store is blocked, use the official
   installer from <https://www.python.org/downloads/windows/>.
2. **Get the project**: go to
   <https://github.com/SID-6921/human-typer-mvp>, click green **Code →
   Download ZIP**, extract anywhere.
3. **Double-click `Run.bat`** in the extracted folder.
   - First launch (~30 s): creates a private Python environment in `.venv\`
     and installs the one dependency (`pynput`).
   - Every launch after: the GUI opens immediately.

To uninstall: delete the folder.

### Option 3 — Fully offline (air-gapped office laptop)

Best for: **no internet on the target laptop**.

On any PC that *does* have internet:

```powershell
# inside the extracted folder, on the online PC:
powershell -ExecutionPolicy Bypass -File .\Download-Wheels.ps1
```

This creates a `vendor\` folder containing all needed wheels. Copy the entire
project folder (now including `vendor\`) to the offline laptop via USB.
Double-click `Run.bat` there — it auto-detects `vendor\` and installs from it
with no internet access.

---

## Using the app

The window has four things:

| Control                | What it does                                                |
|------------------------|-------------------------------------------------------------|
| **Big text area**      | Paste the text you want typed.                              |
| **Profile** dropdown   | `natural` / `fast` / `robotic` / `careful` — preset styles. |
| **Speed (WPM)** slider | Override the profile's speed on the fly.                    |
| **Typos %** slider     | 0 = perfect typing, higher = more human-like mistakes.      |

Buttons:

- **Load file…** — load text from a `.txt` file.
- **Paste from clipboard** — fill the text area from your clipboard.
- **Dry run** — open a preview window and show what *would* be typed. No real
  keystrokes are sent. Recommended for your first run.
- ▶ **Start** — begin the countdown (default 10 s), then type for real.
- ⏸ **Pause (F8)** / ⏹ **Stop (Esc)** — control mid-typing.

**Global hotkeys** (work even when the GUI isn't focused, so you can always
take back control):

| Key   | Action          |
|-------|-----------------|
| **F8**  | Pause / Resume |
| **Esc** | Stop          |

Your last-used **profile, speed, typo %, countdown, and window size** are
remembered automatically in `%APPDATA%\human-typer\config.json` and restored
the next time you open the app.

### A typical run

1. Open Word (or the web form / remote desktop / etc.) and click into the
   text field you want filled.
2. Switch to the human-typer window. Paste your text. Pick a profile.
3. Click **Start**.
4. **Within 10 seconds, click back into your target field** and leave it
   focused.
5. The tool types your text into wherever your cursor is, with realistic
   pauses and (optionally) the occasional auto-corrected typo.

---

## Profiles cheat sheet

You almost never need to edit these — the GUI sliders override them.

| Profile  | Speed     | Typos | Auto-corrects | Best for |
|----------|-----------|-------|---------------|----------|
| natural  | ~60 WPM   | ~2.5% | yes           | Looks like a real person. Default. |
| fast     | ~120 WPM  | ~0.5% | yes           | Quick but still human-ish. |
| robotic  | ~90 WPM   | 0%    | n/a           | Constant speed, zero mistakes. |
| careful  | ~35 WPM   | 0%    | n/a           | Slow, deliberate, fragile forms / slow RDP. |

Profiles are plain JSON files inside the package
(`src/human_typer/profiles/*.json`). Fields:

```json
{
  "wpm": 60,                  // words per minute (5 chars = 1 word)
  "wpm_jitter": 0.30,         // 0..1 random speed variation
  "typo_rate": 0.025,         // 0..1 chance per letter
  "auto_correct": true,       // backspace + retype after a typo
  "correction_delay_ms": 180,
  "thinking_pauses": true,    // longer pauses at punctuation / newlines
  "newline_pause_ms": 350,
  "punct_pause_ms": 120,
  "shift_pause_ms": 25
}
```

---

## Power-user CLI (optional)

If you'd rather drive it from the terminal:

```powershell
.\.venv\Scripts\python.exe -m human_typer --text "hello world"
.\.venv\Scripts\python.exe -m human_typer --file mytext.txt --profile natural --countdown 10
.\.venv\Scripts\python.exe -m human_typer --file mytext.txt --wpm 90 --typo-rate 0.01 --dry-run
```

`--profile` accepts a bundled name (`natural`, `fast`, `robotic`, `careful`)
or a path to your own JSON file.

---

## Safety

- **Only sends keystrokes.** It does not read your screen, your clipboard
  (unless you click *Paste from clipboard* yourself), or the target app's
  contents.
- **No network calls.** There is no network code in the project.
- Types into **whatever window has focus** when the countdown ends — always
  confirm the right window is focused.
- **Esc** stops it instantly.

---

## Troubleshooting

**`Run.bat` flashes and closes**
Open PowerShell in the folder and run `python --version`. If Python isn't
recognised, install it from the Microsoft Store and reopen PowerShell.

**Typing goes into the wrong window**
You didn't focus the target window during the countdown. Press **Esc** to
stop, increase the countdown in the GUI (or `--countdown 15` on the CLI),
try again.

**Nothing happens after countdown**
Some remote-desktop / VM / Citrix clients only accept input once you click
*inside* the window (not just bring it forward). Click into the actual field
first.

**It's typing way too slowly / too fast**
Drag the **Speed (WPM)** slider. Or set `--wpm 90` on the CLI.

**Corporate proxy blocks `pip install`**
Either use the prebuilt `.exe` (Option 1) or set the proxy before launching
`Run.bat`:
```powershell
$env:HTTPS_PROXY = "http://proxy.company.local:8080"
$env:HTTP_PROXY  = "http://proxy.company.local:8080"
.\Run.bat
```
Or use the offline-wheels path (Option 3) and skip the network entirely.

**I want to stop *right now***
Press **Esc**.

---

## What's inside

```
human-typer-mvp/
├── src/human_typer/
│   ├── gui.py            # Tkinter GUI (primary entry point)
│   ├── cli.py            # CLI (power users)
│   ├── engine.py         # timing, typos, auto-corrections
│   ├── keyboard.py       # real keystroke backend + dry-run backend
│   ├── profile.py        # JSON profile loader
│   ├── settings.py       # remembers last-used preferences
│   ├── hotkeys.py        # global F8 / Esc listener
│   └── profiles/         # natural / fast / robotic / careful JSON
├── tests/                # pytest suite (uses dry-run backend, no real keys)
├── .github/workflows/    # builds the Windows .exe on every tag
├── Run.bat               # one-click launcher (auto-creates .venv)
├── Download-Wheels.ps1   # prepare an offline-install bundle
├── pyproject.toml
└── README.md
```

---

## License

MIT — see [LICENSE](LICENSE).
