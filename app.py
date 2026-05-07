import streamlit as st
from audio_recorder_streamlit import audio_recorder # Correct import
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import speech_recognition as sr
from io import BytesIO

def main():
    st.title(" Multi-Language Audio Hub")
    st.subheader("Record -> Extract -> Translate -> Speak")

    # 1. Audio Recording Section
    st.write("### 1. Record Audio")
    audio = audiorecorder("Click to Record", "Click to Stop")
    
    if len(audio) > 0:
        # Playback recorded audio
        st.audio(audio.export().read())
        
        # 2. Language Selection
        st.write("### 2. Configure Translation")
        col1, col2 = st.columns(2)
        
        with col1:
            src_lang = st.selectbox("Source Language (Auto-detect available)", 
                                    ["auto"] + list(LANGUAGES.values()))
        with col2:
            target_lang = st.selectbox("Target Language", list(LANGUAGES.values()))

        if st.button("Process Audio"):
            with st.spinner("Processing..."):
                # Save audio to a buffer for processing
                wav_io = BytesIO()
                audio.export(wav_io, format="wav")
                wav_io.seek(0)

                # 3. Speech to Text (Extraction)
                recognizer = sr.Recognizer()
                with sr.AudioFile(wav_io) as source:
                    audio_data = recognizer.record(source)
                    try:
                        extracted_text = recognizer.recognize_google(audio_data)
                        st.success(f"**Extracted Text:** {extracted_text}")
                        
                        # 4. Translation
                        translator = Translator()
                        # Get lang code from value
                        dest_code = [k for k, v in LANGUAGES.items() if v == target_lang][0]
                        translated = translator.translate(extracted_text, dest=dest_code)
                        
                        st.info(f"**Translated Text ({target_lang}):** {translated.text}")

                        # 5. Text to Speech (Conversion)
                        tts = gTTS(text=translated.text, lang=dest_code)
                        tts_fp = BytesIO()
                        tts.write_to_fp(tts_fp)
                        
                        st.write("### 3. Play Translated Audio")
                        st.audio(tts_fp)

                    except Exception as e:
                        st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
