import streamlit as st
from groq import Groq
import tempfile

API_KEY = "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"
client = Groq(api_key=API_KEY)

st.title("Voice Note Recorder & Transcriber (Groq Whisper)")

# Use st.audio to play uploaded/recorded audio
# For recording, we will use streamlit-webrtc or a JS-based widget.

st.write("### Record your voice note:")

# Using st.file_uploader as a fallback for audio upload or you can integrate streamlit-webrtc for recording

audio_bytes = st.file_uploader("Upload a voice note (.wav or .m4a)", type=["wav", "m4a", "mp3"])

if audio_bytes is not None:
    st.audio(audio_bytes)

    # Save to temp file for sending to API
    with tempfile.NamedTemporaryFile(suffix=".m4a", delete=False) as tmp:
        tmp.write(audio_bytes.read())
        tmp.flush()

        with open(tmp.name, "rb") as f:
            with st.spinner("Transcribing your voice note..."):
                transcription = client.audio.transcriptions.create(
                    file=(tmp.name, f.read()),
                    model="whisper-large-v3",
                    response_format="verbose_json",
                )
                text = transcription.get("text", "No transcription found.")
                st.write("### Transcription:")
                st.write(text)
