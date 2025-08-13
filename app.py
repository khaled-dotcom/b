import streamlit as st
from groq import Groq

API_KEY = "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"

client = Groq(api_key=API_KEY)

st.title(" khaled Transcription")

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
