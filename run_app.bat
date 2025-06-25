@echo off
setlocal enabledelayedexpansion

REM Directorio del entorno virtual
set "VENV_DIR=%~dp0venv"

REM Crear entorno si no existe
IF NOT EXIST "%VENV_DIR%" (
    python -m venv "%VENV_DIR%"
    IF ERRORLEVEL 1 (
        echo ❌ Error creando el entorno virtual.
        goto end
    )
)

REM Activar entorno
CALL "%VENV_DIR%\Scripts\activate.bat"
IF ERRORLEVEL 1 (
    echo ❌ Error activando entorno virtual.
    goto end
)

REM Asegurar pip actualizado
python -m pip install --upgrade pip || goto end

REM Instalar requirements principales (si existe el archivo)
IF EXIST "requirements.txt" (
    pip install -r requirements.txt || goto end
)

REM Instalar requirements secundarios (si existe)
IF EXIST "requirements.conversion.txt" (
    pip install -r requirements.conversion.txt || goto end
)

REM Instalar los módulos críticos directamente
pip install gradio moviepy || goto end
pip install -e . || goto end

REM Lanzar la app
python gradio_app.py || goto end

:end
echo.
echo 🟢 Script terminado. Presiona una tecla para salir...
pause >nul
