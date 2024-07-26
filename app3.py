#This includes progress bar and download button

import streamlit as st
import google.generativeai as genai
import tempfile
import time


genai.configure(api_key='AIzaSyCBgyKZNK-WAuPbF8rWu9_eqJvyUY7By5A')
def transcribe(audio_file, language, format_type):
  try:
    your_file = genai.upload_file(path=audio_file)
    prompt = f"Act as a speech recognizer expert. Listen carefully to the following audio file in {language}. Provide a complete transcript in {format_type} format."
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    response = model.generate_content([prompt, your_file])
    return response.text
  except RuntimeError as e:
    if "Invalid binary data format" in str(e):
        st.error("Unsupported audio file format. Please upload a supported file (e.g., MP3, WAV, FLAC).")
    else:
        st.error(f"An error occurred during transcription: {e}")
        return None

def translate(audio_file, language, format_type):
  try:
    your_file = genai.upload_file(path=audio_file)
    prompt = f"Listen carefully to the following audio file in {language}. Translate it to English in {format_type} format."
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    response = model.generate_content([prompt, your_file])
    return response.text
  except RuntimeError as e:
    if "Invalid binary data format" in str(e):
        st.error("Unsupported audio file format. Please upload a supported file (e.g., MP3, WAV, FLAC).")
    else:
        st.error(f"An error occurred during transcription: {e}")
        return None


def main():
    st.title("⏯Audio Transcription📝 and Translation▶")

    # Add sidebar
    with st.sidebar:
        st.header("About 📆")
        st.write("This tool lets you upload your audio file and select between transcription or translation. Based on your choice, it processes the audio and provides the results. The generated text can be downloaded for your convenience.")
        
        st.header("Developed By")
        st.write("NICTU, LBSNAA for educational and learning purpose")
        # Main content with improved layout
        col1, col2 = st.columns([2, 3])

        with col1:
            # Image or logo
            st.image("https://www.lbsnaa.gov.in/images/lbsnaa-logo.png")

        st.header("Share Feedback on")
        st.write("nictu@lbsnaa.gov.in")

        # # Add social media icons with hyperlinks
        # col3, col4, col5 = st.columns([1, 1, 1])
        # with col3:
            
        #     st.write("Facebook Icon](https://www.flaticon.com/free-icon/facebook-f-logo_310004)[/]")  # Replace with your Facebook icon URL
        #     st.markdown("[fblbs.com](https://www.facebook.com/p/LBSNAA-100064810655288/)", unsafe_allow_html=True)  # Hyperlink for Facebook
        # with col4:
            
        #     st.write("Twitter Icon](https://www.flaticon.com/free-icon/twitter_310009)[/]")  # Replace with your Twitter icon URL
        #     st.markdown("[twtlbs.com](twtlbs.com)", unsafe_allow_html=True)  # Hyperlink for Twitter
        # with col5:
            
        #     st.write("YouTube Icon](https://www.flaticon.com/free-icon/youtube_310012)[/]")  # Replace with your YouTube icon URL
        #     st.markdown("[ytlbs.com](ytlbs.com)", unsafe_allow_html=True)  # Hyperlink for YouTube
    

    audio_file = st.file_uploader("Upload an audio file")

    if audio_file is not None:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_file.write(audio_file.read())
            audio_path = temp_file.name

        language = st.text_input("Enter the language of the audio")

        format_options = ["Conversation style, accurately identify speakers", "Paragraph", "Bullet points","Summary"]
        selected_format = st.selectbox("Choose output format", format_options)

        option = st.selectbox("Choose an option", ["Transcribe", "Translate"])

        if st.button("Process"):
            try:
                progress_bar = st.progress(0)
                # Simulate some processing time
                progress_bar = st.progress(0)
                # Simulate some processing time
                for i in range(100):
                    time.sleep(0.1)
                    progress_bar.progress(i / 100)  # Update progress using progress() method
            except Exception as e:
                st.error(f"An error occurred: {e}")


            if option == "Transcribe":
                transcript = transcribe(audio_path, language, selected_format)
                st.text_area("Transcript", transcript)
                # Add a download button
                st.download_button("Download Transcript", transcript)
            elif option == "Translate":
                translation = translate(audio_path, language, selected_format)
                st.text_area("Translation", translation)
                # Add a download button
                st.download_button("Download Translation", translation)

if __name__ == "__main__":
  main()