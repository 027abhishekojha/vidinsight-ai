# 🎥 VidInsight AI — Offline Video Intelligence System

🔗 **Live Demo:** https://vidinsight-ai.streamlit.app/

VidInsight AI is a fully offline, AI-powered video intelligence system that transcribes multimedia content and extracts meaningful insights using local Large Language Models (LLMs).

Built with a strong focus on **privacy, performance, and zero external API dependency**, it enables users to transform raw video/audio content into structured, actionable knowledge — entirely on their local machine.

---

## 🚀 Project Overview

VidInsight AI bridges the gap between unstructured video data and intelligent analysis by combining:

- High-speed transcription
- Local LLM-powered summarization
- Interactive querying interface

Unlike cloud-based tools, this system ensures:

- 🔒 **Data Privacy (100% local execution)**
- ⚡ **Low latency processing**
- 💸 **Zero API cost**

---

## ✨ Key Features

- 🎤 **Accurate Transcription**
  Converts video/audio into text using Faster-Whisper (optimized for speed & efficiency)
- 🧠 **AI-Powered Insights**
  Generates summaries, key points, and insights using local LLMs via Ollama (Llama 3 / Mistral)
- 💬 **Interactive Chat Interface**
  ChatGPT-like UI built with Streamlit
- 📁 **Multi-Video Support**
  Process and analyze multiple files
- 🔍 **Semantic Search (Optional)**
  Query transcripts using ChromaDB
- 🔒 **Fully Offline System**
  No internet/API dependency after setup

---

## 🏗️ System Architecture

Video Input → FFmpeg → Audio Extraction → Faster-Whisper → Transcript → Ollama → Insights → Streamlit UI

---

## 🛠️ Tech Stack

- Backend: Python
- UI: Streamlit
- Speech-to-Text: Faster-Whisper
- LLM Engine: Ollama (Llama 3 / Mistral)
- Vector DB: ChromaDB (Optional)
- Media Processing: FFmpeg

---

## ⚙️ Prerequisites

- Python 3.9+
- pip
- Git
- FFmpeg
- Ollama

---

## 📦 Installation & Setup

### 1. Clone Repo

git clone https://github.com/yourusername/vidinsight-ai.git
cd vidinsight-ai

### 2. Create Virtual Environment

python -m venv venv

Activate:

- Windows: venv\Scripts\activate
- Mac/Linux: source venv/bin/activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Install External Tools

- Install FFmpeg and add to PATH
- Install Ollama → https://ollama.com/

Pull model:
ollama pull mistral

### 5. Run App

streamlit run app.py

Open:
http://localhost:8501

---

## 🧩 Troubleshooting

- FFmpeg not found → Add to PATH
- Ollama not running → ollama serve
- Model missing → ollama pull mistral
- Slow performance → Use smaller models or GPU

---

## 📄 License

MIT License
