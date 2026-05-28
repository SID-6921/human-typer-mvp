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

    if exist "vendor" (
        echo [setup] Offline mode: installing from local 'vendor' folder...
        ".venv\Scripts\python.exe" -m pip install --no-index --find-links vendor --upgrade pip setuptools wheel --quiet
        ".venv\Scripts\python.exe" -m pip install --no-index --find-links vendor -e . --quiet
    ) else (
        echo [setup] Online mode: installing dependency 'pynput' from PyPI...
        ".venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
        ".venv\Scripts\python.exe" -m pip install -e . --quiet
    )
    if errorlevel 1 (
        echo.
        echo ERROR: pip install failed.
        echo - If you are on a corporate network, set HTTPS_PROXY / HTTP_PROXY.
        echo - Or run Download-Wheels.ps1 on an online PC, copy this folder over,
        echo   and try again (offline mode will be used automatically).
        pause
        exit /b 1
    )
    echo [setup] Done.
)

start "" ".venv\Scripts\pythonw.exe" -m human_typer.gui
endlocal
