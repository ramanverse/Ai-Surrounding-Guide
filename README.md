<div align="center">
  <h1>AI Surroundings Guide</h1>
  <p>An accessible, AI-powered computer vision assistant designed to help the visually impaired understand their physical surroundings through natural language and instant audio feedback.</p>
  <p><b>By Raman</b></p>
  
  <a href="https://ultralytics.com/">
  <img src="https://img.shields.io/badge/YOLOv8-Vision-green?style=for-the-badge">
</a>

<a href="https://groq.com">
  <img src="https://img.shields.io/badge/Groq-Llama-black?style=for-the-badge">
</a>

<a href="https://opencv.org">
  <img src="https://img.shields.io/badge/OpenCV-Computer_Vision-red?style=for-the-badge">
</a>
</div>

---

## 🎯 The Problem & Solution
Navigating dynamic environments is a constant challenge for the visually impaired. Traditional object detection models provide raw coordinates and bounding boxes, which are unhelpful to an end user. 

**AI Surroundings Guide** solves this by fusing real-time **Computer Vision (YOLOv8)** with **Large Language Models (Llama 3.2 Vision)** to translate spatial coordinates into natural, human-like sentences, which are then instantly spoken aloud using the Web Speech API.

## ✨ Key Features
- **Real-Time Spatial Awareness**: Detects objects, calculates their relative proximity, and determines their direction (left/center/right).
- **Cognitive Scene Translation**: Feeds raw bounding-box data and images to an LLM via the Groq API to generate intuitive, context-aware descriptions.
- **Zero-Latency Audio**: Uses browser-native Text-to-Speech (TTS) for instantaneous audio feedback without backend processing delays.
- **Edge-Ready Architecture**: Modular design separating the perception layer (YOLO) from the cognition layer (LLM), making it easy to deploy on edge devices or cloud platforms.

## 🛠️ Technical Architecture & Stack

### AI & Machine Learning
* **YOLOv8s (Ultralytics):** Highly optimized object detection model for fast, local inference.
* **Llama 3.2 Vision (via Groq):** High-speed multimodal LLM used to verify YOLO's output and synthesize natural language descriptions.
* **OpenCV & NumPy:** For image array manipulation and spatial mathematics.

### Backend & Infrastructure
* **FastAPI:** High-performance async Python backend routing image buffers between AI services.
* **Gunicorn / Uvicorn:** Production-ready server configuration.
* **Docker:** Fully containerized for agnostic deployment across AWS, Hugging Face, or Render.

### Frontend
* **Vanilla JavaScript & HTML5:** Lightweight, dependency-free frontend leveraging the MediaDevices API for webcam access and SpeechSynthesis API for TTS.

---

## 🚀 How It Works
1. **Perception**: The user taps a button, and a frame from their camera is sent to the FastAPI backend.
2. **Analysis**: YOLOv8 scans the image, identifying objects and computing their bounding box areas to estimate proximity and direction.
3. **Cognition**: The spatial data + the image are forwarded to the Llama Vision model via Groq's ultra-fast API. The LLM verifies the objects and crafts a conversational description.
4. **Action**: The backend returns the text string, and the frontend instantly reads it aloud to the user.

---

## 💻 Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ramanverse/AI-Surroundings-Guide.git
   cd AI-Surroundings-Guide
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables:**
   Rename `.env.example` to `.env` and add your Groq API Key:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

4. **Run the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access the Application:**
   Open your browser and navigate to `http://localhost:8000/`.

---

<div align="center">
  <i>Built by Raman — Making the world more accessible through Artificial Intelligence.</i>
</div>
