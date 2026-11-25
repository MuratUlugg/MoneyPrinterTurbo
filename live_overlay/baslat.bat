@echo off
rem Hediye Arenasi: ilk calistirmada kurar, sonra paneli acar. Python 3.11+ gerekir (python.org).
cd /d "%~dp0\.."
if not exist live_overlay\.venv (
  echo Ilk kurulum yapiliyor, birkac dakika surebilir...
  python -m venv live_overlay\.venv || (echo Python bulunamadi. python.org adresinden kurun. & pause & exit /b 1)
  live_overlay\.venv\Scripts\python -m pip install --upgrade pip
  live_overlay\.venv\Scripts\python -m pip install -r live_overlay\requirements.txt || (echo Kurulum basarisiz. & pause & exit /b 1)
)
start "" http://127.0.0.1:8765/
live_overlay\.venv\Scripts\python -m live_overlay.server %*
pause
