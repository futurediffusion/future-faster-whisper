import os
import shutil
import tempfile

import gradio as gr
from moviepy.editor import VideoFileClip
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
        with VideoFileClip(file_path) as video:
            video.audio.write_audiofile(audio_path, verbose=False, logger=None)

    segments, _ = model.transcribe(audio_path)
    text = "".join(segment.text for segment in segments)

    if temp_dir:
        shutil.rmtree(temp_dir)

    return text


def main():
    interface = gr.Interface(
        fn=transcribe,
        inputs=gr.File(label="Audio or Video (.mp3, .wav, .mp4)", type="file"),
        outputs=gr.Textbox(label="Transcription"),
        title="faster-whisper Transcription",
    )
    interface.launch()


if __name__ == "__main__":
    main()
