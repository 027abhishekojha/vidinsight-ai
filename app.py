import os
import streamlit as st
from pipeline.transcribe import transcribe
from pipeline.summarize import ask_llm

st.title("🎥 Local Video AI Analyzer")

video_dir = "data/videos"
os.makedirs(video_dir, exist_ok=True)

uploaded_file = st.file_uploader(
    "Upload Video",
    type=["mp4", "mkv", "avi", "mov", "ts"]
)

if uploaded_file:
    # ✅ Keep original extension
    file_extension = uploaded_file.name.split(".")[-1]
    video_path = os.path.join(video_dir, f"temp.{file_extension}")

    # ✅ Save correctly
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("Video uploaded!")

    if st.button("Process Video"):
        with st.spinner("Transcribing..."): 
            text = transcribe(video_path)   # ✅ FIX HERE

        st.text_area("Transcript", text, height=200)

        prompt = f"""
        Analyze this transcript and provide:

        1. Summary
        2. Key insights
        3. Actionable points

        Transcript:
        {text}
        """

        with st.spinner("Analyzing..."):
            output = ask_llm(prompt)

        st.subheader("Insights")
        st.write(output)