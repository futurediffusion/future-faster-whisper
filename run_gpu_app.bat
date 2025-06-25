@echo off
setlocal enabledelayedexpansion

set "VENV_DIR=%~dp0venv"

IF NOT EXIST "%VENV_DIR%" (
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo ❌ Error creando el entorno virtual.
        goto end
    )
)

call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo ❌ Error activando el entorno virtual.
    goto end
)

python -m pip install --upgrade pip
pip install gradio imageio-ffmpeg

REM Paso 1: instala las librerias NVIDIA en el entorno virtual
pip install nvidia-cudnn-cu12==9.5.0.50
pip install nvidia-cuda-nvrtc-cu12==12.4.127
pip install nvidia-cuda-runtime-cu12==12.4.127
pip install nvidia-cublas-cu12==12.4.5.8

REM Paso 3: instala PyTorch segun la version de Python
for /f "delims=" %%v in ('python -c "import sys;print(f'{sys.version_info[0]}.{sys.version_info[1]}')"') do set PYVER=%%v
if "%PYVER%"=="3.11" (
    pip install https://download.pytorch.org/whl/cu124/torch-2.5.0%2Bcu124-cp311-cp311-win_amd64.whl
    pip install https://download.pytorch.org/whl/cu124/torchaudio-2.5.0%2Bcu124-cp311-cp311-win_amd64.whl
) else (
    pip install https://download.pytorch.org/whl/cu124/torch-2.5.0%2Bcu124-cp312-cp312-win_amd64.whl
    pip install https://download.pytorch.org/whl/cu124/torchaudio-2.5.0%2Bcu124-cp312-cp312-win_amd64.whl
)

REM Paso 4: reinstala faster-whisper sin deps
pip install -e . --no-deps

python gradio_app.py
if errorlevel 1 (
    echo ❌ Error ejecutando gradio_app.py
)

:end
echo.
echo 🟢 Script terminado. Presiona una tecla para salir...
pause >nul
