import os
import time
import subprocess
import streamlit as st
from groq import Groq
import imageio_ffmpeg as ffmpeg  

os.environ["GROQ_API_KEY"] = "your_groq_api_key_here"
groq_client = Groq(api_key="")


def download_video(url):
    output_file = "youtube_audio.mp3"
    ffmpeg_path = ffmpeg.get_ffmpeg_exe()
    cmd = [
        "yt-dlp",
        "--ffmpeg-location", ffmpeg_path,
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "-o", output_file,
        url
    ]
    subprocess.run(cmd, check=True)
    return output_file

def transcribe_with_groq(file_path):
    with open(file_path, "rb") as audio_file:
        transcription = groq_client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=audio_file
        )
    return transcription.text

def chunk_text(text, max_chars=3000):
    words = text.split()
    chunks, current_chunk = [], []
    current_len = 0
    for word in words:
        current_chunk.append(word)
        current_len += len(word) + 1
        if current_len >= max_chars:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_len = 0
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def summarize_with_groq(transcript_text):
    chunks = chunk_text(transcript_text)
    summaries = []
    for chunk in chunks:
        prompt = f"Summarize the following part of a YouTube video transcript:\n\n{chunk}\n\nSummary:"
        completion = groq_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )
        summaries.append(completion.choices[0].message.content)
    final_prompt = "Combine these partial summaries into a final concise summary:\n\n" + "\n\n".join(summaries)
    final_completion = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": final_prompt}],
        temperature=0.3,
        max_tokens=500
    )
    return final_completion.choices[0].message.content

def answer_question_with_groq(transcript_text, question):
    chat_prompt = f"You are an assistant answering questions based on the following YouTube video transcript:\n\n{transcript_text}\n\nQuestion: {question}\n\nAnswer:"
    chat_completion = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": chat_prompt}],
        temperature=0.2,
        max_tokens=500
    )
    return chat_completion.choices[0].message.content

# ===== STREAMLIT APP =====
st.set_page_config(layout="wide")
st.title("YouTube Video Summarizer 🎥 + Chat 💬 by vivek kumar")

youtube_url = st.text_input("Enter YouTube URL", value=st.session_state.get("youtube_url", ""))

if st.button("Submit"):
    st.session_state["youtube_url"] = youtube_url
    start_time = time.time()
    try:
        file_path = download_video(youtube_url)
        transcript_text = transcribe_with_groq(file_path)
        summary = summarize_with_groq(transcript_text)

        st.session_state["transcript"] = transcript_text
        st.session_state["summary"] = summary
        st.session_state["process_time"] = time.time() - start_time

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Display video, summary, and chat if we have data
if "transcript" in st.session_state and "summary" in st.session_state:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.video(st.session_state["youtube_url"])
    with col2:
        st.header("Summary")
        st.success(st.session_state["summary"])
        with st.expander("📜 Full Transcript"):
            st.write(st.session_state["transcript"])
        st.write(f"⏱ Time taken: {st.session_state['process_time']:.2f} seconds")

    # Chat section
    st.subheader("💬 Ask a question about this video")
    user_q = st.text_input("Your question:", key="user_q_input")
    if st.button("Ask"):
        if st.session_state.get("transcript"):
            answer = answer_question_with_groq(st.session_state["transcript"], user_q)
            st.markdown(f"**Answer:** {answer}")
