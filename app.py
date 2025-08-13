import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()  # Loads .env file if present (for local testing)

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    st.error("Please set the GROQ_API_KEY environment variable.")
    st.stop()

client = Groq(api_key=API_KEY)

st.title("Groq Whisper Large V3 Audio Transcription")

uploaded_file = st.file_uploader("Upload an audio file (.m4a)", type=["m4a"])

if uploaded_file is not None:
    with st.spinner("Transcribing audio..."):
        transcription = client.audio.transcriptions.create(
            file=(uploaded_file.name, uploaded_file.read()),
            model="whisper-large-v3",
            response_format="verbose_json",
        )
        text = transcription.get("text", "No transcription found.")
        st.write("### Transcription:")
        st.write(text)
