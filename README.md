# human-typer-mvp

A small Windows desktop tool that **types text for you, key by key**, into
whatever text field is currently focused — a Word document, a web form, a
remote-desktop window, a kiosk app, anything that accepts keyboard input.

It is useful when:

- Paste (`Ctrl+V`) is blocked or disabled in an app.
- You need text entered into a remote session that doesn't share clipboard.
- You want a long passage typed with realistic human pauses (for accessibility,
  demos, QA testing, screen recordings, etc.).

> Only use it on systems where you are allowed to automate keyboard input.
> Do **not** use it to bypass anti-cheat software, exam-proctoring tools, or
> any platform's Terms of Service.

---

## Table of contents

1. [What you need (one-time setup)](#1-what-you-need-one-time-setup)
2. [Get the project (two ways)](#2-get-the-project-two-ways)
3. [Install the tool](#3-install-the-tool)
4. [Pick an accuracy profile](#4-pick-an-accuracy-profile)
5. [Put the text you want typed](#5-put-the-text-you-want-typed)
6. [Run it — the actual typing](#6-run-it--the-actual-typing)
7. [Hotkeys while it's running](#7-hotkeys-while-its-running)
8. [Other ways to feed input](#8-other-ways-to-feed-input)
9. [Customising a profile](#9-customising-a-profile)
10. [Troubleshooting](#10-troubleshooting)
11. [Project layout & how it works](#11-project-layout--how-it-works)
12. [Safety & permitted use](#12-safety--permitted-use)

---

## 1. What you need (one-time setup)

You only need **one** thing: **Python 3.10 or newer**.

You do **not** need Git, Visual Studio, admin rights, or any compiler.

### Install Python (if you don't already have it)

1. Open the Microsoft Store on your Windows laptop.
2. Search for **"Python 3.12"** (publisher: *Python Software Foundation*).
3. Click **Get / Install**. No admin password needed.
4. Open PowerShell and confirm:
   ```powershell
   python --version
   ```
   You should see something like `Python 3.12.x`.

If your office laptop blocks the Microsoft Store, ask IT to install Python, or
download the official installer from <https://www.python.org/downloads/windows/>.

---

## 2. Get the project (two ways)

### Option A — No Git needed (recommended for office laptops)

1. Open this page in your browser: <https://github.com/SID-6921/human-typer-mvp>
2. Click the green **`Code`** button.
3. Click **`Download ZIP`**.
4. Save the file (e.g. to `Downloads`).
5. Right-click the ZIP → **Extract All…** → choose a folder, e.g.
   `C:\Users\<you>\Documents\human-typer-mvp`.

You now have a folder called `human-typer-mvp` (or `human-typer-mvp-main`).
Everything in the rest of this README assumes you are inside that folder.

### Option B — With Git (if it's already installed)

```powershell
git clone https://github.com/SID-6921/human-typer-mvp
cd human-typer-mvp
```

---

## 3. Install the tool

Open PowerShell, then **`cd`** into the project folder. Example:

```powershell
cd C:\Users\<you>\Documents\human-typer-mvp
```

(If you used the ZIP and the folder is called `human-typer-mvp-main`, use that
name instead.)

Now create an isolated Python environment and install the tool into it. This
keeps it from touching your system Python or anything IT has set up:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e .
```

That's it. The tool is installed inside the `.venv` folder. To uninstall later,
just delete the project folder.

> **Why a venv?** Because office laptops often block global `pip install`.
> A venv is just a folder — no admin rights, no registry changes, nothing IT
> will object to.

---

## 4. Pick an accuracy profile

A **profile** is a small JSON file in the `profiles/` folder that controls how
the tool types: speed, typo rate, pauses, etc. Four are included:

| File                       | Speed     | Typos | Auto-corrects | Best for |
|----------------------------|-----------|-------|---------------|----------|
| `profiles/natural.json`    | ~60 WPM   | ~2.5% | yes           | Looks like a real person typing. Default choice. |
| `profiles/fast.json`       | ~120 WPM  | ~0.5% | yes           | You want it done quickly but still human-ish. |
| `profiles/robotic.json`    | ~90 WPM   | 0%    | n/a           | Constant speed, no mistakes. Fastest "clean" mode. |
| `profiles/careful.json`    | ~35 WPM   | 0%    | n/a           | Slow, deliberate, for fragile forms or slow remote sessions. |

You don't have to edit them. Pick one and use it as-is.

---

## 5. Put the text you want typed

The simplest way: create a file called **`input.txt`** in the project folder
and paste your text into it.

In PowerShell:

```powershell
notepad input.txt
```

Notepad opens. Paste your text, save, close.

> A starter file called `input.txt.example` is included. You can copy it:
> ```powershell
> Copy-Item input.txt.example input.txt
> ```

---

## 6. Run it — the actual typing

This is the moment where keystrokes are sent for real. Follow the steps in
order — the **countdown matters**, because whatever window is focused when the
countdown ends is where the typing will go.

### Step-by-step

1. Make sure your target application is already open (Word, the web form,
   the remote session, etc.) and that there is a visible text cursor in the
   field you want typed into.
2. In PowerShell, from inside the project folder, run:
   ```powershell
   .\.venv\Scripts\python.exe -m human_typer.cli `
       --file input.txt `
       --profile profiles\natural.json `
       --countdown 10
   ```
   (The backticks `` ` `` are PowerShell line continuations. You can also put
   the whole command on one line.)
3. The terminal prints:
   ```
   Focus the target field. Typing starts in 10s (F8 pause/resume, Esc abort)...
     10...
     9...
     ...
   ```
4. **Immediately click into your target text field** (Word, browser, etc.).
   Leave that window in the foreground.
5. When the countdown hits zero, the tool starts sending keystrokes into
   whatever has focus.
6. When it finishes, the terminal prints `Done.`

### A safer first run: `--dry-run`

If you've never used it before, do a dry-run first. It prints what it *would*
type into the terminal, without sending any real keystrokes:

```powershell
.\.venv\Scripts\python.exe -m human_typer.cli --file input.txt --profile profiles\natural.json --dry-run
```

You'll see the essay appear in your PowerShell window, including the simulated
typos getting backspaced. No real keys are sent anywhere.

---

## 7. Hotkeys while it's running

These work no matter which window is focused — so you can always take back
control:

| Key   | Action               |
|-------|----------------------|
| **F8**  | Pause / Resume     |
| **Esc** | Abort immediately  |

If you press **Esc**, the terminal prints `Aborted.` and exits.

---

## 8. Other ways to feed input

You don't have to use `input.txt`. The CLI accepts three input sources:

```powershell
# 1. From a file (most common)
.\.venv\Scripts\python.exe -m human_typer.cli --file input.txt --profile profiles\natural.json

# 2. Inline string
.\.venv\Scripts\python.exe -m human_typer.cli --text "hello world" --profile profiles\natural.json

# 3. From the clipboard, via stdin
Get-Clipboard | .\.venv\Scripts\python.exe -m human_typer.cli --stdin --profile profiles\natural.json
```

You can also override profile values on the command line:

```powershell
# Force 200 WPM regardless of profile
.\.venv\Scripts\python.exe -m human_typer.cli --file input.txt --profile profiles\natural.json --wpm 200

# Disable typos
.\.venv\Scripts\python.exe -m human_typer.cli --file input.txt --profile profiles\natural.json --typo-rate 0
```

Full option list:

```
--file PATH          Path to a text file to type.
--text STRING        Literal text to type.
--stdin              Read text from stdin.
--profile PATH       Path to a JSON accuracy profile.
--countdown SECONDS  Seconds before typing starts (minimum 2, default 5).
--wpm N              Override profile WPM.
--typo-rate 0..1     Override profile typo rate.
--dry-run            Print planned keystrokes; do not send keys.
```

---

## 9. Customising a profile

A profile is a plain JSON file. Copy one and edit it:

```powershell
Copy-Item profiles\natural.json profiles\my-profile.json
notepad profiles\my-profile.json
```

Fields and what they do:

```json
{
  "wpm": 60,                  // target words per minute (5 chars = 1 word)
  "wpm_jitter": 0.30,         // 0..1, random speed variation per keystroke
  "typo_rate": 0.025,         // 0..1, chance of mistyping each letter
  "auto_correct": true,       // backspace + retype after a typo
  "correction_delay_ms": 180, // pause before correcting a typo
  "thinking_pauses": true,    // longer pauses at punctuation / newlines
  "newline_pause_ms": 350,    // extra pause after Enter
  "punct_pause_ms": 120,      // extra pause after , . ; : ! ? )
  "shift_pause_ms": 25        // extra pause for uppercase letters
}
```

Then use it:

```powershell
.\.venv\Scripts\python.exe -m human_typer.cli --file input.txt --profile profiles\my-profile.json
```

---

## 10. Troubleshooting

**`python` is not recognised**
The Microsoft Store install adds `python` to PATH for your user, but a new
PowerShell window is needed for it to pick up. Close PowerShell, reopen, try
again. If still missing, run `where.exe python` to see what's installed.

**`pip install` fails with SSL / proxy errors on a corporate network**
Your laptop is likely behind a proxy. Ask IT for the proxy URL, then:
```powershell
$env:HTTPS_PROXY = "http://proxy.company.local:8080"
$env:HTTP_PROXY  = "http://proxy.company.local:8080"
.\.venv\Scripts\python.exe -m pip install -e .
```

**Typing goes into the wrong window**
You didn't focus the target window during the countdown. Press **Esc** to
abort, increase `--countdown` (e.g. `--countdown 15`), and try again.

**Nothing happens / no keystrokes appear**
- Confirm the target field actually accepts keyboard input (some web apps
  steal focus on load).
- Try `--dry-run` first to confirm the tool itself is working.
- Some remote-desktop / virtual-machine clients capture input only when their
  window is *clicked into*, not just on top. Click inside the field, don't
  just bring the window forward.

**It's typing way too slowly / too fast**
Use `--wpm` to override, e.g. `--wpm 90`. Or edit a profile (see §9).

**I want to stop *right now***
Press **Esc**. The tool exits within ~50 ms.

---

## 11. Project layout & how it works

```
human-typer-mvp/
├── src/human_typer/
│   ├── cli.py        # command-line entry point
│   ├── engine.py     # timing, typos, auto-corrections
│   ├── keyboard.py   # real keystroke backend (pynput) + dry-run backend
│   ├── profile.py    # load and validate JSON profiles
│   └── hotkeys.py    # global F8 / Esc listener
├── profiles/         # natural.json, fast.json, robotic.json, careful.json
├── tests/            # pytest suite (uses dry-run backend, no real keys)
├── input.txt.example # starter file — copy to input.txt
├── pyproject.toml
└── README.md
```

How it actually types:

1. `cli.py` reads your text and chosen profile.
2. A 2+ second countdown gives you time to focus the target field.
3. `engine.py` walks the text character by character. For each character it:
   - waits a delay derived from the profile's WPM (with random jitter),
   - sometimes injects a plausible nearby-key typo and (optionally) backspaces
     and retypes,
   - adds extra pauses at punctuation / line breaks / shifted letters,
   - sends the keystroke via `keyboard.py` (real, using `pynput`, or dry-run).
4. `hotkeys.py` runs a background listener so **F8** and **Esc** always work.

---

## 12. Safety & permitted use

- The tool **only sends keystrokes**. It does not read your screen, your
  clipboard contents (unless you pipe them in yourself), or the target
  application's data.
- It does not phone home. There is no network code in the project.
- It will type into **whatever window is focused** at the end of the countdown.
  Always confirm the right window is focused before the countdown ends.
- Acceptable uses include: accessibility, personal productivity, QA test
  automation, demos and screen recordings, entering text into systems where
  paste is disabled for usability (not policy) reasons.
- Do **not** use it to defeat anti-cheat, exam-proctoring, or platform Terms
  of Service. The author accepts no responsibility for misuse.

---

## License

MIT — see [LICENSE](LICENSE).
