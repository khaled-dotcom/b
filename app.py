import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import numpy as np
import tempfile
from groq import Groq

API_KEY = "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"
client = Groq(api_key=API_KEY)

st.title("Record Voice Note and Transcribe (Groq Whisper)")

st.write("Click **Start** to record from your microphone.")

# Buffer to store recorded audio frames
audio_frames = []

def audio_frame_callback(frame: av.AudioFrame):
    audio_frames.append(frame)
    return frame

webrtc_ctx = webrtc_streamer(
    key="audio-recorder",
    mode="sendrecv",
    audio_frame_callback=audio_frame_callback,
    media_stream_constraints={"audio": True, "video": False},
    audio_receiver_size=1024,
    async_processing=True,
)

if webrtc_ctx.state.playing:
    st.write("Recording...")

if st.button("Stop and Transcribe"):
    if not audio_frames:
        st.warning("No audio recorded yet!")
    else:
        # Convert frames to a single WAV file
        # Combine frames into bytes
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
            container = av.open(tmp_wav.name, mode='w')
            stream = container.add_stream('pcm_s16le', rate=48000)
            stream.channels = 1

            for frame in audio_frames:
                for packet in stream.encode(frame):
                    container.mux(packet)
            # Flush encoder
            for packet in stream.encode():
                container.mux(packet)
            container.close()
            tmp_wav.flush()

            st.audio(tmp_wav.name, format="audio/wav")
            
            # Send recorded audio to Groq API
            with open(tmp_wav.name, "rb") as f:
                with st.spinner("Transcribing..."):
                    transcription = client.audio.transcriptions.create(
                        file=(tmp_wav.name, f.read()),
                        model="whisper-large-v3",
                        response_format="verbose_json",
                    )
                    text = transcription.get("text", "No transcription found.")
                    st.write("### Transcription:")
                    st.write(text)

