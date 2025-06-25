import os
import shutil
import tempfile

import gradio as gr
from faster_whisper import WhisperModel
from moviepy.editor import VideoFileClip

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
        try:
            with VideoFileClip(file_path) as video:
                video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        except Exception as e:
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
