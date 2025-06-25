@echo off

REM Directory where the virtual environment will be created
set "VENV_DIR=%~dp0venv"

REM Create the virtual environment if it does not exist
IF NOT EXIST "%VENV_DIR%" (
    python -m venv "%VENV_DIR%"
)

REM Activate the virtual environment
CALL "%VENV_DIR%\Scripts\activate"

REM Install python dependencies inside the virtual environment
python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements.conversion.txt
pip install gradio moviepy
pip install -e .

REM Launch the application
python gradio_app.py
