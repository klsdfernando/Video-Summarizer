# 🎬 Video Summarizer CLI
Developed by **klsdfernando**

---

## 📽️ Project Overview
The **Video Summarizer CLI** is an advanced, high-performance tool designed to automate the extraction of insights from video files. It leverages cutting-edge AI to provide both a visual and textual summary, specifically optimized for **NVIDIA RTX 40-series GPUs** using CUDA acceleration.

Whether you are summarizing a long lecture, a technical meeting, or a YouTube tutorial, this tool handles the heavy lifting of media processing and AI analysis locally on your machine.

---

## 🧠 Step-by-Step: How It Works
The script executes a sophisticated 4-stage pipeline to ensure accuracy and speed:

1.  **Visual Highlight Extraction**: 
    The tool uses **OpenCV** to scan the video stream. It extracts high-resolution frames at a regular interval (customizable via CLI). These screenshots provide a visual storyboard of the video's content.
2.  **Audio Stream Extraction**: 
    Using **MoviePy**, the audio track is isolated from the video container and saved as a high-quality temporary MP3 file for processing.
3.  **GPU-Accelerated Transcription**: 
    The audio is fed into **OpenAI Whisper**. The script automatically detects your **RTX 4070** and uses CUDA to transcribe speech to text at up to 10x real-time speed.
4.  **Intelligent Summarization**: 
    The resulting transcript is sent to a Large Language Model (LLM). The script formats a specialized prompt to extract key takeaways, main points, and a concise final summary.

---

## 🛠️ Technical Framework Stack
| Framework | Purpose | Description |
| :--- | :--- | :--- |
| **OpenAI Whisper** | Transcription | The industry standard for local, high-precision speech-to-text. |
| **MoviePy** | Media Handling | Handles complex video/audio extraction tasks. |
| **OpenCV (cv2)** | Computer Vision | Efficiently manages frame-by-frame video decoding. |
| **PyTorch (CUDA)** | AI Engine | Provides the underlying GPU acceleration for the RTX 4070. |
| **OpenAI SDK** | API Interface | Standardized communication with LM Studio, Ollama, and Cloud APIs. |
| **FFmpeg** | Core Engine | The "Swiss Army Knife" of media processing used under the hood. |

---

## 🚀 Installation & Setup

### 1. Prerequisites
- **Python 3.8+**
- **FFmpeg**: Must be installed and reachable in your System PATH (`ffmpeg -version` should work).
- **CUDA Toolkit**: Recommended for NVIDIA GPU users.

### 2. Setup Commands
```bash
# Install core dependencies
pip install -r requirements.txt

# Setup GPU Acceleration (Crucial for RTX 4070)
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

---

## 🖥️ Usage & Customization

### 📂 Detailed CLI Arguments
| Argument | Flag | Default | Description |
| :--- | :--- | :--- | :--- |
| **Input Video** | *(Required)* | - | Path to the video file you want to summarize. |
| **Interval** | `-i`, `--interval` | `10` | **Screenshot frequency** (e.g., set to `5` for more frames). |
| **Output Dir** | `-o`, `--output` | `output` | Folder where all results will be saved. |
| **Whisper Model**| `-m`, `--model` | `base` | `tiny`, `base`, `small`, `medium`, `large`. |
| **Max Tokens** | `--max-tokens` | `1000` | **Output Length Control**: Max tokens for the summary. |
| **LLM URL** | `--llm-url` | `http://localhost:1234/v1` | Base URL for your LLM (LM Studio/Ollama). |
| **LLM Key** | `--llm-key` | - | API Key for cloud providers (optional for local). |
| **LLM Model** | `--llm-model` | `local-model`| The name of the AI model to call. |

---

## 🔌 Connecting Different AI Platforms

This tool is highly flexible and works with almost any OpenAI-compatible API.

### 1. Using LM Studio (Default)
- Start LM Studio and go to the **Local Server** tab.
- Click **Start Server**.
- Simply run the script; it will use the default `http://localhost:1234/v1`.

### 2. Using Ollama
Ollama now supports the OpenAI API format natively.
- Ensure Ollama is running (`ollama serve`).
- Use the following flags:
```bash
python video_summarizer.py "video.mp4" --llm-url http://localhost:11434/v1 --llm-model llama3
```

### 3. Using Cloud AI (OpenAI/Anthropic)
```bash
python video_summarizer.py "video.mp4" --llm-url https://api.openai.com/v1 --llm-key sk-xxxx --llm-model gpt-4
```

---

## 📝 How to Change Specific Settings

### 🕒 Changing Screenshot Frequency
To capture a screenshot every 5 seconds instead of 10:
```bash
python video_summarizer.py "my_video.mp4" --interval 5
```

### 📏 Controlling Summary Length (Token Size)
To get a longer, more detailed summary (e.g., 2000 tokens):
```bash
python video_summarizer.py "my_video.mp4" --max-tokens 2000
```

---

## 📁 Output Results
All results are neatly organized in the output folder:
- `screenshots/`: Visual storyboard of the video.
- `transcript.txt`: Complete text version of everything said.
- `summary.txt`: The AI-generated analysis.

---

### Created by **klsdfernando**
*Empowering video content analysis with Local AI.*

#   V i d e o - S u m m a r i z e r  