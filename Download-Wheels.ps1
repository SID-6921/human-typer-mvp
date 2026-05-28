# Run this on a machine WITH internet access to download all wheels into vendor\
# Then copy the whole project folder (including vendor\) to the offline laptop.
# Run.bat will detect vendor\ and install from it without needing internet.
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$vendor = Join-Path $here "vendor"
New-Item -ItemType Directory -Force -Path $vendor | Out-Null

Write-Host "Downloading wheels into $vendor ..."
python -m pip download `
    --dest $vendor `
    --only-binary=:all: `
    --python-version 3.12 `
    --platform win_amd64 `
    pynput pip setuptools wheel

Write-Host ""
Write-Host "Done. Copy the whole project folder (including vendor\) to the offline laptop."
Write-Host "Then double-click Run.bat there."
