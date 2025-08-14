# 🎥 Video Summarizer + Q&A Chatbot
![Image](https://github.com/user-attachments/assets/d8aead1f-c34f-421a-bb82-505ae319484f)

This project is a **YouTube Video Summarizer and Q&A assistant** built with **Python**, **Streamlit**, and **Groq API**.  
It **downloads the original YouTube audio**, **transcribes it using Groq's Whisper model**, and **summarizes** the content.  
You can also **chat with the AI** to ask questions about the video.

> ⚡ **Note**: We are **NOT** using YouTube's auto-generated captions.  
> The transcript is generated **directly from the original audio** using Groq's transcription model for better accuracy.

---

## ✨ Features
- **🎯 Direct Audio Transcription**  
  Extracts and transcribes the **original YouTube audio** using **Groq Whisper** (no reliance on captions).
- **📝 Automatic Summarization**  
  Splits long transcripts into chunks, summarizes each part, and combines them into a final concise summary.
- **💬 Interactive Q&A**  
  Ask natural language questions about the video and get context-aware answers from Groq's large language model.
- **📜 Full Transcript View**  
  Expandable transcript section to see every word from the original video.
- **🎥 Video Player Integration**  
  Watch the YouTube video directly in the app alongside the summary.

---

## 🛠 Tech Stack
- **[Streamlit](https://streamlit.io/)** – Interactive web UI
- **[Groq API](https://groq.com/)** – Whisper transcription & GPT-style text generation
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** – Download original audio from YouTube
- **[imageio-ffmpeg](https://pypi.org/project/imageio-ffmpeg/)** – Handle audio extraction and format conversion
- **Python** – Backend logic

---

### 1️⃣ Clone the repo
```bash
git clone https://github.com/bevivek12/yt_summarizer.git
cd youtube-summarizer


