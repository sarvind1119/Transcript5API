#added the choice for user to select the resultant format style
import streamlit as st
import google.generativeai as genai
import tempfile
import os
from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
def transcribe(audio_file, language, format_type):
  your_file = genai.upload_file(path=audio_file)
  prompt = f"Listen carefully to the following audio file in {language}. Provide a complete transcript in {format_type} format."
  model = genai.GenerativeModel('models/gemini-1.5-flash')
  response = model.generate_content([prompt, your_file])
  return response.text

def translate(audio_file, language, format_type):
  your_file = genai.upload_file(path=audio_file)
  prompt = f"Listen carefully to the following audio file in {language}. Translate it to English in {format_type} format."
  model = genai.GenerativeModel('models/gemini-1.5-flash')
  response = model.generate_content([prompt, your_file])
  return response.text

def main():
  st.title("Audio Transcription and Translation")

  audio_file = st.file_uploader("Upload an audio file")

  if audio_file is not None:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
      temp_file.write(audio_file.read())
      audio_path = temp_file.name

    language = st.text_input("Enter the language of the audio")

    format_options = ["Conversation style", "Paragraph", "Bullet points"]
    selected_format = st.selectbox("Choose output format", format_options)

    option = st.selectbox("Choose an option", ["Transcribe", "Translate"])

    if st.button("Process"):
      if option == "Transcribe":
        transcript = transcribe(audio_path, language, selected_format)
        st.text_area("Transcript", transcript)
      elif option == "Translate":
        translation = translate(audio_path, language, selected_format)
        st.text_area("Translation", translation)

if __name__ == "__main__":
  main()
