import os
import shutil
import subprocess
import tempfile

import gradio as gr
import imageio_ffmpeg
from faster_whisper import WhisperModel

MODEL_SIZE = os.getenv("MODEL_SIZE", "small")
model = WhisperModel(MODEL_SIZE)


def transcribe(file_obj):
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
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    segments, _ = model.transcribe(audio_path)
    text = "".join(segment.text for segment in segments)

    if temp_dir:
        shutil.rmtree(temp_dir)

    return text


def main():
    interface = gr.Interface(
        fn=transcribe,
        inputs=gr.File(label="Audio or Video (.mp3, .wav, .mp4)", type="filepath"),
        outputs=gr.Textbox(label="Transcription"),
        title="faster-whisper Transcription",
    )
    interface.launch()


if __name__ == "__main__":
    main()
