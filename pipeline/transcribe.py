from concurrent.futures import ThreadPoolExecutor
from faster_whisper import WhisperModel
import subprocess
import os
import shutil


import torch
print(torch.cuda.is_available())


# ⚡ Use GPU if available
# model = WhisperModel("tiny", device="cuda", compute_type="float16")
model = WhisperModel(
    "small",
    device="cuda" if torch.cuda.is_available() else "cpu",
    compute_type="float16" if torch.cuda.is_available() else "int8"
)

def process_chunk(chunk_path):
    segments, _ = model.transcribe(chunk_path)
    return " ".join([seg.text for seg in segments])


def transcribe_parallel(chunk_files):
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_chunk, chunk_files))

    return " ".join(results)

###def extract_audio(video_path, audio_path):
    print("Step 1: Extracting audio...")
    result = subprocess.run(
        [
            "ffmpeg", "-i", video_path,
            "-vn", "-ac", "1", "-ar", "16000",
            audio_path
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.returncode != 0:
        raise Exception(f"FFmpeg error: {result.stderr.decode()}")

###

def extract_audio(video_path, audio_path):
    print("Video path:", video_path)
    print("Audio path:", audio_path)
    command = [
        "ffmpeg",
        "-y",                     # ✅ auto overwrite (IMPORTANT)
        "-fflags", "+genpts",
        "-loglevel", "info",     # reduce noise
        "-i", video_path,
        "-vn",
        "-ac", "1",
        "-ar", "16000",
        "-f", "mp3",
        audio_path
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.returncode != 0:
        raise Exception(f"FFmpeg error:\n{result.stderr.decode()}")

def split_audio(audio_path):
    print("Step 2: Splitting audio...")
    os.makedirs("data/chunks", exist_ok=True)

    result = subprocess.run(
        [
            "ffmpeg",
            "-i", audio_path,
            "-f", "segment",
            "-segment_time", "300",
            "-c", "copy",
            "data/chunks/output_%03d.mp3"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if result.returncode != 0:
        raise Exception(f"Chunking error: {result.stderr.decode()}")



def transcribe(video_path):
    print("Step 3: Transcribing chunks...")
    # ✅ Check input file
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"{video_path} not found")

    os.makedirs("data/audio", exist_ok=True)

    audio_path = "data/audio/temp.mp3"

    # ✅ CLEAN OLD CHUNKS (correct place)
    if os.path.exists("data/chunks"):
        shutil.rmtree("data/chunks")

    # Step 1: Extract audio
    extract_audio(video_path, audio_path)

    # Step 2: Split audio
    split_audio(audio_path)

    # ✅ Prepare chunk paths
    chunk_files = [
        os.path.join("data/chunks", f)
        for f in sorted(os.listdir("data/chunks"))
        if f.endswith(".mp3")
    ]

    # ✅ APPLY PARALLEL PROCESSING HERE
    full_text = transcribe_parallel(chunk_files)

    chunk_files = sorted(os.listdir("data/chunks"))

    for i, file in enumerate(chunk_files):
        if file.endswith(".mp3"):
            chunk_path = os.path.join("data/chunks", file)

            print(f"Processing chunk {i+1}/{len(chunk_files)}...")
            try:
                segments, _ = model.transcribe(chunk_path)
            except Exception as e:
                print("Error:", e)

            chunk_text = " ".join([seg.text for seg in segments])
            full_text += chunk_text + " "

    return full_text.strip()