import streamlit as st
import google.generativeai as genai
import tempfile

#GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key='AIzaSyCBgyKZNK-WAuPbF8rWu9_eqJvyUY7By5A')
def transcribe(audio_file, language):
  your_file = genai.upload_file(path=audio_file)
  prompt = f"Listen carefully to the following audio file in {language}. This is a debate among 5 people. Provide a complete transcript in conversation style, Speaker wise "
  model = genai.GenerativeModel('models/gemini-1.5-flash')
  response = model.generate_content([prompt, your_file])
  return response.text

def translate(audio_file, language):
  your_file = genai.upload_file(path=audio_file)
  prompt = f"Listen carefully to the following audio file in {language}. Translate it to English."
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

    option = st.selectbox("Choose an option", ["Transcribe", "Translate"])

    if st.button("Process"):
      if option == "Transcribe":
        transcript = transcribe(audio_path, language)
        st.text_area("Transcript", transcript)
      elif option == "Translate":
        translation = translate(audio_path, language)
        st.text_area("Translation", translation)

if __name__ == "__main__":
  main()