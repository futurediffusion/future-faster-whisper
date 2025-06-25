import os
import sys
from pathlib import Path


def set_cuda_paths():
    venv_base = Path(sys.executable).parent.parent
    nvidia_base_path = venv_base / "Lib" / "site-packages" / "nvidia"
    cuda_path = nvidia_base_path / "cuda_runtime" / "bin"
    cublas_path = nvidia_base_path / "cublas" / "bin"
    cudnn_path = nvidia_base_path / "cudnn" / "bin"
    paths_to_add = [str(cuda_path), str(cublas_path), str(cudnn_path)]
    env_vars = ["CUDA_PATH", "CUDA_PATH_V12_4", "PATH"]

    for env_var in env_vars:
        current_value = os.environ.get(env_var, "")
        new_value = os.pathsep.join(
            paths_to_add + [current_value] if current_value else paths_to_add
        )
        os.environ[env_var] = new_value


set_cuda_paths()

import shutil
import subprocess
import tempfile

import gradio as gr
import imageio_ffmpeg
from faster_whisper import WhisperModel

model_error = None
try:
    model = WhisperModel("large-v3", device="cuda", compute_type="float16")
except (RuntimeError, OSError) as e:
    model = None
    model_error = (
        f"Error inicializando el modelo en GPU: {e}\n"
        "Verifica que CUDA y cuDNN est\xE9n instalados. "
        "Puedes ejecutar en CPU si el problema persiste."
    )


def transcribe(file_obj):
    if model is None:
        return model_error

    file_path = getattr(file_obj, "name", file_obj)
    ext = os.path.splitext(file_path)[1].lower()

    temp_dir = None
    audio_path = file_path

    if ext == ".mp4":
        temp_dir = tempfile.mkdtemp()
        audio_path = os.path.join(temp_dir, "audio.wav")
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        cmd = [
            ffmpeg_exe,
            "-y",
            "-i",
            file_path,
            "-vn",
            "-acodec",
            "pcm_s16le",
            "-ar",
            "16000",
            "-ac",
            "1",
            audio_path,
        ]
        try:
            subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            shutil.rmtree(temp_dir, ignore_errors=True)
            return f"Error extrayendo audio: {e}"

    try:
        segments, _ = model.transcribe(audio_path)
        text = "".join(segment.text for segment in segments)
    except (RuntimeError, OSError) as e:
        text = (
            f"Error al ejecutar en GPU: {e}\n"
            "Quiz\xE1 cuDNN no est\xE9 configurado. Considera usar la CPU."
        )
    finally:
        if temp_dir:
            shutil.rmtree(temp_dir, ignore_errors=True)

    return text


def main():
    interface = gr.Interface(
        fn=transcribe,
        inputs=gr.File(label="Audio o Video (.mp3, .wav, .mp4)", type="filepath"),
        outputs=gr.Textbox(label="Transcripci\xF3n"),
        title="faster-whisper GPU App",
    )
    interface.launch()


if __name__ == "__main__":
    main()
