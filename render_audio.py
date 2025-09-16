import streamlit as st
import os

def render_audio_podcast():
    st.header("Audio Clips - Podcast for Stewards")
    audio_dir = "audio/podcast_for_stewards"

    if not os.path.exists(audio_dir):
        st.error(f"Directory '{audio_dir}' does not exist. Please create it and add MP3 files.")
        return

    mp3_files = [f for f in os.listdir(audio_dir) if f.lower().endswith('.mp3')]
    if not mp3_files:
        st.info("No audio clips found. Please add MP3 files to the audio_clips directory.")
        return

    selected_mp3 = st.selectbox("Choose an audio clip to play:", mp3_files)

    if selected_mp3:
        audio_path = os.path.join(audio_dir, selected_mp3)
        with open(audio_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
