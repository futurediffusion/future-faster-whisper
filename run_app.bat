@echo off
IF NOT EXIST venv (
    python -m venv venv
)
CALL venv\Scripts\activate
pip install --upgrade pip
pip install gradio moviepy
pip install -e .
python gradio_app.py
