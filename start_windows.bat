@echo off

REM Create venv if it doesn't exist
if not exist venv (
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate.bat

REM Run the WebUI
python webui.py
