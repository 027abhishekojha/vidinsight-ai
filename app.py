import os
import streamlit as st
from pipeline.transcribe import transcribe
from pipeline.summarize import ask_llm

# -------------------------------
# UI Title
# -------------------------------
st.title("🎥 VidInsight AI — Offline Video Intelligence System")

# -------------------------------
# Ensure folders exist
# -------------------------------
video_dir = "data/videos"
os.makedirs(video_dir, exist_ok=True)

# -------------------------------
# Multi File Upload
# -------------------------------
uploaded_files = st.file_uploader(
    "Upload Videos",
    type=["mp4", "mkv", "avi", "mov", "ts"],
    accept_multiple_files=True
)

# -------------------------------
# Save Uploaded Files
# -------------------------------
saved_paths = []

if uploaded_files:
    for file in uploaded_files:
        file_path = os.path.join(video_dir, file.name)

        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

        saved_paths.append(file_path)

    st.success(f"✅ {len(saved_paths)} video(s) uploaded successfully!")

# -------------------------------
# Process Button
# -------------------------------
if saved_paths and st.button("🚀 Process All Videos"):

    overall_progress = st.progress(0)
    status = st.empty()

    try:
        total_videos = len(saved_paths)

        for idx, video_path in enumerate(saved_paths):

            video_name = os.path.basename(video_path)

            status.text(f"🎬 Processing: {video_name}")

            # -------------------------------
            # Step 1: Transcription
            # -------------------------------
            text = transcribe(video_path)

            st.subheader(f"📄 Transcript — {video_name}")
            st.text_area(
                f"Transcript Output ({video_name})",
                text,
                height=200
            )

            # -------------------------------
            # Step 2: LLM Analysis
            # -------------------------------
            prompt = f"""
            Analyze this transcript and provide:

            1. Summary
            2. Key insights
            3. Actionable points

            Transcript:
            {text[:5000]}
            """

            output = ask_llm(prompt)

            st.subheader(f"💡 Insights — {video_name}")
            st.write(output)

            # -------------------------------
            # Update Progress
            # -------------------------------
            progress_value = int(((idx + 1) / total_videos) * 100)
            overall_progress.progress(progress_value)

        status.text("✅ All videos processed successfully!")

    except Exception as e:
        st.error(f"❌ Error occurred: {str(e)}")
        status.text("❌ Failed")