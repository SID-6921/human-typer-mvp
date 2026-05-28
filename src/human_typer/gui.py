"""Tkinter GUI — the primary, friendly entry point."""
from __future__ import annotations

import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from .engine import ControlState, type_text
from .keyboard import DryRunBackend, PynputBackend
from .profile import BUNDLED, Profile
from .settings import Settings


APP_TITLE = "human-typer"


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("720x560")
        self.root.minsize(620, 480)

        self.control = ControlState()
        self.worker: threading.Thread | None = None
        self.settings = Settings.load()
        if self.settings.window_geometry:
            try:
                self.root.geometry(self.settings.window_geometry)
            except Exception:
                pass

        self._build_ui()
        self._start_hotkeys()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ---------- UI ----------
    def _build_ui(self) -> None:
        pad = {"padx": 10, "pady": 6}

        # Top: text area
        top = ttk.LabelFrame(self.root, text="Text to type")
        top.pack(fill="both", expand=True, **pad)

        self.text = tk.Text(top, wrap="word", height=14, undo=True)
        self.text.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        sb = ttk.Scrollbar(top, command=self.text.yview)
        sb.pack(side="right", fill="y", padx=(0, 8), pady=8)
        self.text.config(yscrollcommand=sb.set)

        # Row: load buttons
        loadrow = ttk.Frame(self.root)
        loadrow.pack(fill="x", **pad)
        ttk.Button(loadrow, text="Load file…", command=self.on_load_file).pack(side="left")
        ttk.Button(loadrow, text="Paste from clipboard", command=self.on_paste_clip).pack(side="left", padx=6)
        ttk.Button(loadrow, text="Clear", command=lambda: self.text.delete("1.0", "end")).pack(side="left")

        # Controls
        ctrl = ttk.LabelFrame(self.root, text="How to type")
        ctrl.pack(fill="x", **pad)

        ttk.Label(ctrl, text="Profile:").grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.profile_var = tk.StringVar(value=self.settings.profile)
        ttk.Combobox(ctrl, textvariable=self.profile_var, values=sorted(BUNDLED),
                     state="readonly", width=12).grid(row=0, column=1, sticky="w", pady=6)

        ttk.Label(ctrl, text="Speed (WPM):").grid(row=0, column=2, sticky="e", padx=(20, 4))
        self.wpm_var = tk.IntVar(value=self.settings.wpm)
        ttk.Scale(ctrl, from_=20, to=200, orient="horizontal", variable=self.wpm_var,
                  length=180, command=lambda _=None: self.wpm_lbl.config(text=str(self.wpm_var.get()))
                  ).grid(row=0, column=3, sticky="w")
        self.wpm_lbl = ttk.Label(ctrl, text=str(self.settings.wpm), width=4)
        self.wpm_lbl.grid(row=0, column=4, sticky="w")

        ttk.Label(ctrl, text="Typos %:").grid(row=1, column=2, sticky="e", padx=(20, 4))
        self.typo_var = tk.DoubleVar(value=self.settings.typo_percent)
        ttk.Scale(ctrl, from_=0, to=15, orient="horizontal", variable=self.typo_var,
                  length=180, command=lambda _=None: self.typo_lbl.config(text=f"{self.typo_var.get():.1f}")
                  ).grid(row=1, column=3, sticky="w")
        self.typo_lbl = ttk.Label(ctrl, text=f"{self.settings.typo_percent:.1f}", width=4)
        self.typo_lbl.grid(row=1, column=4, sticky="w")

        ttk.Label(ctrl, text="Countdown (s):").grid(row=1, column=0, sticky="w", padx=8, pady=6)
        self.countdown_var = tk.IntVar(value=self.settings.countdown)
        ttk.Spinbox(ctrl, from_=2, to=60, textvariable=self.countdown_var, width=5).grid(row=1, column=1, sticky="w")

        # Action row
        actions = ttk.Frame(self.root)
        actions.pack(fill="x", **pad)
        self.start_btn = ttk.Button(actions, text="▶  Start", command=self.on_start)
        self.start_btn.pack(side="left")
        self.pause_btn = ttk.Button(actions, text="⏸  Pause (F8)", command=self.on_pause, state="disabled")
        self.pause_btn.pack(side="left", padx=6)
        self.stop_btn = ttk.Button(actions, text="⏹  Stop (Esc)", command=self.on_stop, state="disabled")
        self.stop_btn.pack(side="left")
        ttk.Button(actions, text="🧪 Dry run", command=self.on_dry_run).pack(side="right")

        # Status
        self.status_var = tk.StringVar(value="Ready. Paste text, pick a profile, click Start.")
        ttk.Label(self.root, textvariable=self.status_var, anchor="w",
                  relief="sunken").pack(fill="x", side="bottom")

    # ---------- helpers ----------
    def _get_text(self) -> str:
        return self.text.get("1.0", "end-1c")

    def _get_profile(self) -> Profile:
        prof = Profile.load(self.profile_var.get())
        prof.wpm = float(self.wpm_var.get())
        prof.typo_rate = float(self.typo_var.get()) / 100.0
        prof.validate()
        return prof

    def _set_running(self, running: bool) -> None:
        state = "disabled" if running else "normal"
        self.start_btn.config(state=state)
        self.pause_btn.config(state=("normal" if running else "disabled"))
        self.stop_btn.config(state=("normal" if running else "disabled"))

    # ---------- actions ----------
    def on_load_file(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = f.read()
        except Exception as e:
            messagebox.showerror(APP_TITLE, f"Could not read file:\n{e}")
            return
        self.text.delete("1.0", "end")
        self.text.insert("1.0", data)
        self.status_var.set(f"Loaded {path}")

    def on_paste_clip(self) -> None:
        try:
            data = self.root.clipboard_get()
        except tk.TclError:
            messagebox.showinfo(APP_TITLE, "Clipboard is empty or not text.")
            return
        self.text.delete("1.0", "end")
        self.text.insert("1.0", data)
        self.status_var.set("Pasted from clipboard.")

    def on_pause(self) -> None:
        self.control.paused = not self.control.paused
        self.status_var.set("Paused (F8 to resume)." if self.control.paused else "Resumed.")
        self.pause_btn.config(text=("▶  Resume (F8)" if self.control.paused else "⏸  Pause (F8)"))

    def on_stop(self) -> None:
        self.control.aborted = True
        self.status_var.set("Stopping…")

    def on_dry_run(self) -> None:
        text = self._get_text()
        if not text:
            messagebox.showinfo(APP_TITLE, "Nothing to type.")
            return
        try:
            profile = self._get_profile()
        except Exception as e:
            messagebox.showerror(APP_TITLE, f"Bad settings:\n{e}")
            return

        win = tk.Toplevel(self.root)
        win.title("Dry run — preview")
        win.geometry("640x420")
        out = tk.Text(win, wrap="word")
        out.pack(fill="both", expand=True)

        def on_char(ch: str) -> None:
            if ch == "\b":
                out.delete("end-2c", "end-1c")
            else:
                out.insert("end", ch)
            out.see("end")

        backend = DryRunBackend(on_char=lambda c: self.root.after(0, on_char, c))

        def run():
            ctl = ControlState()
            type_text(text, backend, profile, control=ctl)
            self.root.after(0, lambda: self.status_var.set("Dry run complete."))

        threading.Thread(target=run, daemon=True).start()
        self.status_var.set("Dry run started…")

    def on_start(self) -> None:
        text = self._get_text()
        if not text.strip():
            messagebox.showinfo(APP_TITLE, "Nothing to type. Paste some text first.")
            return
        try:
            profile = self._get_profile()
        except Exception as e:
            messagebox.showerror(APP_TITLE, f"Bad settings:\n{e}")
            return

        countdown = max(2, int(self.countdown_var.get()))
        self.control = ControlState()
        self._set_running(True)

        def run():
            try:
                backend = PynputBackend()
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(APP_TITLE, f"Could not access keyboard:\n{e}"))
                self.root.after(0, lambda: self._set_running(False))
                return

            for i in range(countdown, 0, -1):
                if self.control.aborted:
                    break
                self.root.after(0, lambda i=i: self.status_var.set(
                    f"Focus the target window — typing in {i}s… (F8 pause, Esc stop)"))
                time.sleep(1)

            if not self.control.aborted:
                self.root.after(0, lambda: self.status_var.set("Typing…  (F8 pause, Esc stop)"))
                type_text(text, backend, profile, control=self.control)

            done_msg = "Stopped." if self.control.aborted else "Done."
            self.root.after(0, lambda: self.status_var.set(done_msg))
            self.root.after(0, lambda: self._set_running(False))
            self.root.after(0, lambda: self.pause_btn.config(text="⏸  Pause (F8)"))

        self.worker = threading.Thread(target=run, daemon=True)
        self.worker.start()

    # ---------- hotkeys ----------
    def _start_hotkeys(self) -> None:
        try:
            from pynput import keyboard  # type: ignore
        except Exception:
            return

        def on_press(key):
            try:
                if key == keyboard.Key.esc:
                    self.control.aborted = True
                elif key == keyboard.Key.f8:
                    # toggle pause from any thread
                    self.root.after(0, self.on_pause)
            except Exception:
                pass

        listener = keyboard.Listener(on_press=on_press)
        listener.daemon = True
        listener.start()

    def _on_close(self) -> None:
        try:
            self.settings.profile = self.profile_var.get()
            self.settings.wpm = int(self.wpm_var.get())
            self.settings.typo_percent = float(self.typo_var.get())
            self.settings.countdown = int(self.countdown_var.get())
            self.settings.window_geometry = self.root.geometry()
            self.settings.save()
        finally:
            self.root.destroy()


def main() -> int:
    root = tk.Tk()
    try:
        ttk.Style().theme_use("vista")
    except Exception:
        pass
    App(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
