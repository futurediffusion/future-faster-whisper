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
pip install -e .

python gradio_app.py
if errorlevel 1 (
    echo ❌ Error ejecutando gradio_app.py
    where cudnn_ops64_9.dll >nul 2>&1
    if errorlevel 1 (
        echo ⚠ Falta cudnn_ops64_9.dll. Instala cuDNN 9 para CUDA 12 desde: https://developer.nvidia.com/rdp/cudnn-download
    )
)

:end
echo.
echo 🟢 Script terminado. Presiona una tecla para salir...
pause >nul
