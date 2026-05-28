# human-typer

**Type any text into any focused window — like a real human typing.**
A tiny Windows app for when paste (`Ctrl+V`) is blocked or unavailable.

> Two-step UX:
> **1.** Double-click `Run.bat` → a small window opens.
> **2.** Paste your text, click **Start**, click into the target field (Word, browser, etc.) within 10 seconds.
>
> That's it. No command line. No Git. Works on a locked-down office laptop.

---

## Install (one time, ~2 minutes)

You have **two ways** to install. Pick whichever your laptop allows.

### Option 1 — Prebuilt single .exe (easiest)

1. Go to <https://github.com/SID-6921/human-typer-mvp/releases/latest>.
2. Download **`human-typer.exe`**.
3. Double-click it. Done — no Python, no install, nothing else.

*(If there's no release yet, use Option 2.)*

### Option 2 — From source (needs Python 3.10+)

1. **Get Python** — Microsoft Store → search **"Python 3.12"** → Install.
   (No admin password needed. If the Store is blocked, get the official
   installer from <https://www.python.org/downloads/windows/>.)
2. **Get this project**:
   - Go to <https://github.com/SID-6921/human-typer-mvp>
   - Click green **Code** → **Download ZIP**
   - Right-click the ZIP → **Extract All…**
3. **Open the extracted folder** and **double-click `Run.bat`**.
   - First launch only: it creates a small private Python environment inside
     the folder and installs one dependency (`pynput`). Takes ~30 seconds.
   - Every launch after that: the GUI opens immediately.

### Option 3 — Fully offline (air-gapped / no-internet office laptop)

Do this on a PC that *does* have internet, once:

```powershell
# inside the extracted folder, on an online PC:
powershell -ExecutionPolicy Bypass -File .\Download-Wheels.ps1
```

That creates a `vendor\` folder with all needed wheels. Copy the whole project
folder (now including `vendor\`) to the offline laptop via USB. Double-click
`Run.bat` there — it automatically installs from `vendor\` without touching
the internet.

To uninstall any of the above: just delete the folder (or the `.exe`).

---

## Using it

The GUI window has four things:

| Control               | What it does                                                |
|-----------------------|-------------------------------------------------------------|
| **Big text area**     | Paste the text you want typed.                              |
| **Profile dropdown**  | `natural` / `fast` / `robotic` / `careful` — preset speeds. |
| **Speed (WPM) slider**| Override profile speed on the fly.                          |
| **Typos % slider**    | 0 = perfect typing, higher = more human-like mistakes.      |

Buttons:

- **Load file…** — load a `.txt` file instead of pasting.
- **Paste from clipboard** — fill the text area from your clipboard.
- **Dry run** — show what *would* be typed inside the GUI; no real keystrokes.
- **Start (10s countdown)** — start a 10-second countdown, then type for real.
- **Pause / Resume** and **Stop** — control mid-typing.

**Global hotkeys** (work even when the GUI isn't focused):

- **F8** — Pause / Resume
- **Esc** — Stop

Your last-used **profile, speed, typo %, countdown, and window size** are
remembered automatically in `%APPDATA%\human-typer\config.json` and restored
the next time you open the app.

### Typical flow

1. Open Word (or the web form, or the remote-desktop window) and click into
   the text field you want filled.
2. Switch to the human-typer window. Paste your text. Pick a profile.
3. Click **Start**.
4. **Within 10 seconds, click back into your target field.**
5. The tool types your text into wherever your cursor is, with realistic
   pauses and (optionally) the occasional auto-corrected typo.

---

## Power-user CLI (optional)

If you prefer the terminal:

```powershell
.\.venv\Scripts\python.exe -m human_typer --text "hello world"
.\.venv\Scripts\python.exe -m human_typer --file mytext.txt --profile natural --countdown 10
.\.venv\Scripts\python.exe -m human_typer --file mytext.txt --wpm 90 --typo-rate 0.01 --dry-run
```

Bundled profiles live in `profiles/`. You can pass either a profile **name**
(`natural`, `fast`, `robotic`, `careful`) or a path to your own JSON file.

---

## Profiles

A profile is a tiny JSON file in `profiles/`. You almost never need to touch
these — the GUI sliders override them. Fields:

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

## Safety

- Only sends keystrokes. No screen reading. No network calls.
- Types into **whatever window has focus** when the countdown ends — always
  confirm the right window is focused.
- **Esc** stops it instantly.
- Use on systems where you're allowed to automate keyboard input. Don't use
  it against anti-cheat, exam-proctoring, or platform Terms of Service.

---

## Troubleshooting

**`Run.bat` flashes and closes**
Open PowerShell in the folder and run `python --version`. If Python isn't
recognised, install it from the Microsoft Store and reopen PowerShell.

**Typing goes into the wrong window**
You didn't focus the target window during the 10s countdown. Press **Esc**
to stop and try again.

**Nothing happens after countdown**
Some remote-desktop clients only accept input after you click *inside* the
window (not just bring it forward). Click into the actual field first.

**Corporate proxy blocks `pip install`**
Set the proxy before launching `Run.bat`:
```powershell
$env:HTTPS_PROXY = "http://proxy.company.local:8080"
$env:HTTP_PROXY  = "http://proxy.company.local:8080"
.\Run.bat
```

---

## License

MIT — see [LICENSE](LICENSE).
