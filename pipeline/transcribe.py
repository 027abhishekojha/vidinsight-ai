import whisper
import subprocess
import os

model = whisper.load_model("base")

def extract_audio(video_path, audio_path):
    result = subprocess.run(
        [
            "ffmpeg", "-i", video_path,
            "-vn", "-acodec", "mp3",
            audio_path
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.returncode != 0:
        print("FFmpeg Error:", result.stderr.decode())
        raise Exception("Audio extraction failed")


def transcribe(video_path):

    # ✅ FIX 3 — ADD HERE (VERY FIRST STEP)
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"{video_path} not found")

    # ✅ Ensure audio folder exists
    audio_dir = "data/audio"
    os.makedirs(audio_dir, exist_ok=True)

    audio_path = os.path.join(audio_dir, "temp.mp3")

    # Extract audio
    extract_audio(video_path, audio_path)

    # Transcribe
    result = model.transcribe(audio_path)

    return result["text"]