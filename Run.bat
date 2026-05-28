@echo off
REM ============================================================
REM  human-typer launcher
REM  - first run: creates .venv and installs dependencies
REM  - every run: launches the GUI
REM ============================================================
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [setup] First-time setup. Creating private Python environment...
    python -m venv .venv
    if errorlevel 1 (
        echo.
        echo ERROR: Python was not found. Install Python 3.10+ from the
        echo Microsoft Store, then close and reopen this folder.
        pause
        exit /b 1
    )
    echo [setup] Installing dependency: pynput ...
    ".venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
    ".venv\Scripts\python.exe" -m pip install -e . --quiet
    if errorlevel 1 (
        echo.
        echo ERROR: pip install failed. If you are on a corporate network,
        echo set HTTPS_PROXY and HTTP_PROXY environment variables, then try
        echo again.
        pause
        exit /b 1
    )
    echo [setup] Done.
)

start "" ".venv\Scripts\pythonw.exe" -m human_typer.gui
endlocal
