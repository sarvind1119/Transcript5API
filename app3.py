# # Improved version: app3_v2.py with long audio chunking support and microphone recording

# import streamlit as st
# import google.generativeai as genai
# import tempfile
# import os
# import pandas as pd
# from dotenv import load_dotenv
# from datetime import datetime
# from textblob import TextBlob
# import traceback
# import zipfile
# from pydub import AudioSegment
# from audiorecorder import audiorecorder

# # Load API key
# load_dotenv()
# GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
# genai.configure(api_key=GOOGLE_API_KEY)

# # Format label mapping
# FORMAT_MAP = {
#     "Conversation style, accurately identify speakers": "conversation",
#     "Paragraph": "paragraph",
#     "Bullet points": "bullet",
#     "Summary": "summary"
# }

# # Initialize model once
# MODEL = genai.GenerativeModel('models/gemini-1.5-flash')

# def split_audio(file_path, max_minutes=25):
#     audio = AudioSegment.from_file(file_path)
#     max_ms = max_minutes * 60 * 1000
#     chunks = [audio[i:i + max_ms] for i in range(0, len(audio), max_ms)]

#     chunk_paths = []
#     for i, chunk in enumerate(chunks):
#         chunk_path = f"{file_path}_part{i+1}.wav"
#         chunk.export(chunk_path, format="wav")
#         chunk_paths.append(chunk_path)
#     return chunk_paths

# def transcribe_or_translate(audio_path, format_type, is_translate=False):
#     results = []
#     chunk_paths = split_audio(audio_path, max_minutes=25)

#     for i, chunk_path in enumerate(chunk_paths):
#         try:
#             uploaded = genai.upload_file(path=chunk_path)
#             task = "Translate it to English" if is_translate else "Provide a complete transcript"
#             prompt = f"Act as a speech recognizer expert. Listen carefully to the following audio file. {task} in {format_type} format."
#             response = MODEL.generate_content([prompt, uploaded])
#             results.append(f"[Part {i+1}]\n{response.text.strip()}\n")
#         except Exception as e:
#             results.append(f"[Error in part {i+1}]: {e}\n")

#     return "\n\n".join(results)

# def analyze_sentiment(text):
#     blob = TextBlob(text)
#     polarity = blob.sentiment.polarity
#     subjectivity = blob.sentiment.subjectivity

#     if polarity > 0.1:
#         return "Positive"
#     elif polarity < -0.1:
#         return "Negative"
#     return "Neutral" if subjectivity < 0.3 else "Mixed"

# def save_results_to_excel(data, filename):
#     df = pd.DataFrame(data)
#     df.to_excel(filename, index=False)
#     return filename

# def save_results_to_text(data, filename):
#     with open(filename, 'w', encoding='utf-8') as f:
#         for entry in data:
#             f.write(f"Audio File: {entry['Audio File Name']}\n")
#             f.write(f"Result: {entry['Transcript/Translation']}\n")
#             f.write(f"Format: {entry['Format Chosen']}\n")
#             f.write(f"Sentiment: {entry['Sentiment']}\n")
#             f.write("-"*50 + "\n\n")
#     return filename

# def save_individual_texts(results):
#     zip_filename = "individual_results.zip"
#     with zipfile.ZipFile(zip_filename, 'w') as zipf:
#         for entry in results:
#             file_name = entry['Audio File Name'].replace(" ", "_") + ".txt"
#             content = f"Transcript/Translation:\n{entry['Transcript/Translation']}\n\nSentiment: {entry['Sentiment']}"
#             with open(file_name, 'w', encoding='utf-8') as f:
#                 f.write(content)
#             zipf.write(file_name)
#             os.remove(file_name)
#     return zip_filename

# def main():
#     st.title("Audio Transcription 📝 and Translation ▶")

#     with st.sidebar:
#         st.header("About 📆")
#         st.write("Upload audio files or record your voice to transcribe or translate. Results are saved to Excel/Text.")
#         st.image("https://www.lbsnaa.gov.in/images/lbsnaa-logo.png")
#         st.write("Developed by NICTU, LBSNAA")

#     input_type = st.radio("Choose Input Type", ["Upload Audio", "Record Audio"])

#     selected_format_label = st.selectbox("Choose output format", list(FORMAT_MAP.keys()))
#     selected_format = FORMAT_MAP[selected_format_label]
#     action = st.selectbox("Choose an option", ["Transcribe", "Translate"])
#     separate_files = st.checkbox("Save each output as individual text file (ZIP)")

#     results = []

#     if input_type == "Upload Audio":
#         audio_files = st.file_uploader("Upload audio files", accept_multiple_files=True, type=["wav", "mp3", "flac"])

#         if audio_files and st.button("Process Uploaded Files"):
#             progress = st.progress(0)

#             for idx, audio in enumerate(audio_files):
#                 try:
#                     suffix = os.path.splitext(audio.name)[1]
#                     with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
#                         tmp.write(audio.read())
#                         audio_path = tmp.name

#                     text = transcribe_or_translate(audio_path, selected_format, action == "Translate")
#                     sentiment = analyze_sentiment(text)

#                     results.append({
#                         "Audio File Name": audio.name,
#                         "Transcript/Translation": text,
#                         "Format Chosen": selected_format_label,
#                         "Sentiment": sentiment
#                     })

#                     progress.progress(int(((idx + 1) / len(audio_files)) * 100))

#                 except Exception as e:
#                     st.error(f"Error with {audio.name}: {e}")
#                     st.text(traceback.format_exc())

#     elif input_type == "Record Audio":
#         st.subheader("🎙️ Click the mic to start/stop recording")
#         audio = audiorecorder("Click to record", "Recording...")

#         if len(audio) > 0:
#             st.audio(audio.tobytes(), format="audio/wav")
#             if st.button("Process Recording"):
#                 try:
#                     with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
#                         tmp.write(audio.tobytes())
#                         audio_path = tmp.name

#                     text = transcribe_or_translate(audio_path, selected_format, action == "Translate")
#                     sentiment = analyze_sentiment(text)

#                     results.append({
#                         "Audio File Name": "Recorded_Audio",
#                         "Transcript/Translation": text,
#                         "Format Chosen": selected_format_label,
#                         "Sentiment": sentiment
#                     })

#                 except Exception as e:
#                     st.error("Error processing recorded audio")
#                     st.text(traceback.format_exc())

#     if results:
#         date_str = datetime.now().strftime("%m_%d_%y")
#         excel_file = save_results_to_excel(results, f"Results_{date_str}.xlsx")
#         text_file = save_results_to_text(results, f"Results_{date_str}.txt")

#         st.success("Processing complete!")
#         with open(excel_file, "rb") as f:
#             st.download_button("Download Excel", f, file_name=excel_file)
#         with open(text_file, "rb") as f:
#             st.download_button("Download Text", f, file_name=text_file)

#         if separate_files:
#             zip_file = save_individual_texts(results)
#             with open(zip_file, "rb") as f:
#                 st.download_button("Download ZIP (individual texts)", f, file_name=zip_file)

# if __name__ == "__main__":
#     main()


# #multiple audio files and save results to Excel

# import streamlit as st
# import google.generativeai as genai
# import tempfile
# import time
# import os
# import pandas as pd
# from dotenv import load_dotenv
# from datetime import datetime
# from textblob import TextBlob
# import streamlit as st

# # hide_streamlit_style = """
# #     <style>
# #         /* Hide Fork and GitHub icons */
# #         [title="Fork this app"], [title="View source on GitHub"] {
# #             display: none !important;
# #         }
# #     </style>
# # """
# # st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# load_dotenv()
# GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
# genai.configure(api_key=GOOGLE_API_KEY)

# # Function to process transcription
# def transcribe(audio_file, format_type):
#     try:
#         your_file = genai.upload_file(path=audio_file)
#         prompt = f"Act as a speech recognizer expert. Listen carefully to the following audio file. Provide a complete transcript in {format_type} format."
#         model = genai.GenerativeModel('models/gemini-1.5-flash')
#         response = model.generate_content([prompt, your_file])
#         return response.text
#     except RuntimeError as e:
#         if "Invalid binary data format" in str(e):
#             st.error("Unsupported audio file format. Please upload a supported file (e.g., MP3, WAV, FLAC).")
#         else:
#             st.error(f"An error occurred during transcription: {e}")
#         return None

# # Function to process translation
# def translate(audio_file, format_type):
#     try:
#         your_file = genai.upload_file(path=audio_file)
#         prompt = f"Listen carefully to the following audio file. Translate it to English in {format_type} format."
#         model = genai.GenerativeModel('models/gemini-1.5-flash')
#         response = model.generate_content([prompt, your_file])
#         return response.text
#     except RuntimeError as e:
#         if "Invalid binary data format" in str(e):
#             st.error("Unsupported audio file format. Please upload a supported file (e.g., MP3, WAV, FLAC).")
#         else:
#             st.error(f"An error occurred during transcription: {e}")
#         return None

# # Analyze sentiment of text
# def analyze_sentiment(text):
#     blob = TextBlob(text)
#     polarity = blob.sentiment.polarity
#     subjectivity = blob.sentiment.subjectivity

#     # Adjusted thresholds for polarity
#     if polarity > 0.1:  # Lower the positive threshold for milder positivity
#         return "Positive"
#     elif polarity < -0.1:  # Lower the negative threshold to avoid false negatives
#         return "Negative"
#     else:
#         # For very neutral text, use subjectivity to decide
#         if subjectivity < 0.3:  # Highly objective text is usually neutral
#             return "Neutral"
#         else:
#             return "Mixed"


# # Save results to Excel
# def save_results_to_excel(data):
#     today_date = datetime.now().strftime("%m_%d_%y")
#     results_filename = f"Results_of_{today_date}.xlsx"
    
#     if os.path.exists(results_filename):
#         existing_data = pd.read_excel(results_filename)
#         new_data = pd.concat([existing_data, pd.DataFrame(data)], ignore_index=True)
#     else:
#         new_data = pd.DataFrame(data)
    
#     new_data.to_excel(results_filename, index=False)
#     return results_filename

# # Save results to text file
# def save_results_to_text(data):
#     today_date = datetime.now().strftime("%m_%d_%y")
#     results_filename = f"Results_of_{today_date}.txt"
    
#     with open(results_filename, 'w') as file:
#         for entry in data:
#             file.write(f"Audio File Name: {entry['Audio File Name']}\n")
#             file.write(f"Transcript/Translation: {entry['Transcript/Translation']}\n")
#             file.write(f"Format Chosen: {entry['Format Chosen']}\n")
#             file.write(f"Sentiment: {entry['Sentiment']}\n")
#             file.write("\n" + "-"*50 + "\n\n")
    
#     return results_filename

# # Main Streamlit app
# def main():
#     st.title("⏯Audio Transcription📝 and Translation▶")

#     # Add sidebar
#     with st.sidebar:
#         st.header("About 📆")
#         st.write("This tool lets you upload your audio file(s) and select between transcription or translation. The results are saved in an Excel file.")
#         st.header("Developed By")
#         st.write("NICTU, LBSNAA for educational and learning purpose")
#         st.image("https://www.lbsnaa.gov.in/images/lbsnaa-logo.png")
#         st.header("Share Feedback on")
#         st.write("nictu@lbsnaa.gov.in")

#     audio_files = st.file_uploader("Upload audio files", accept_multiple_files=True, type=["wav", "mp3", "flac"])

#     if audio_files:
#         format_options = ["Conversation style, accurately identify speakers", "Paragraph", "Bullet points", "Summary"]
#         selected_format = st.selectbox("Choose output format", format_options)

#         option = st.selectbox("Choose an option", ["Transcribe", "Translate"])

#         if st.button("Process"):
#             results_data = []
#             progress_bar = st.progress(0)

#             for idx, audio_file in enumerate(audio_files):
#                 try:
#                     with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
#                         temp_file.write(audio_file.read())
#                         audio_path = temp_file.name

#                     if option == "Transcribe":
#                         result_text = transcribe(audio_path, selected_format)
#                     elif option == "Translate":
#                         result_text = translate(audio_path, selected_format)

#                     sentiment = analyze_sentiment(result_text)

#                     results_data.append({
#                         "Audio File Name": audio_file.name,
#                         "Transcript/Translation": result_text,
#                         "Format Chosen": selected_format,
#                         "Sentiment": sentiment
#                     })

#                     progress_bar.progress(int(((idx + 1) / len(audio_files)) * 100))

#                 except Exception as e:
#                     st.error(f"An error occurred with file {audio_file.name}: {e}")

#             # Save all results to Excel and text file
#             if results_data:
#                 saved_excel_file = save_results_to_excel(results_data)
#                 saved_text_file = save_results_to_text(results_data)
                
#                 st.success(f"Results saved to {saved_excel_file} and {saved_text_file}")

#                 with open(saved_excel_file, "rb") as file:
#                     st.download_button("Download Excel Results", file, file_name=saved_excel_file)
                
#                 with open(saved_text_file, "rb") as file:
#                     st.download_button("Download Text Results", file, file_name=saved_text_file)

# if __name__ == "__main__":
#     main()

#multiple audio files and save results to Excel

import streamlit as st
import google.generativeai as genai
import tempfile
import time
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from textblob import TextBlob
import streamlit as st

# hide_streamlit_style = """
#     <style>
#         /* Hide Fork and GitHub icons */
#         [title="Fork this app"], [title="View source on GitHub"] {
#             display: none !important;
#         }
#     </style>
# """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

load_dotenv()
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Function to process transcription
def transcribe(audio_file, format_type):
    try:
        your_file = genai.upload_file(path=audio_file)
        prompt = f"Act as a speech recognizer expert. Listen carefully to the following audio file. Provide a complete transcript in {format_type} format."
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        response = model.generate_content([prompt, your_file])
        return response.text
    except RuntimeError as e:
        if "Invalid binary data format" in str(e):
            st.error("Unsupported audio file format. Please upload a supported file (e.g., MP3, WAV, FLAC).")
        else:
            st.error(f"An error occurred during transcription: {e}")
        return None

# Function to process translation
def translate(audio_file, format_type):
    try:
        your_file = genai.upload_file(path=audio_file)
        prompt = f"Listen carefully to the following audio file. Translate it to English in {format_type} format."
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        response = model.generate_content([prompt, your_file])
        return response.text
    except RuntimeError as e:
        if "Invalid binary data format" in str(e):
            st.error("Unsupported audio file format. Please upload a supported file (e.g., MP3, WAV, FLAC).")
        else:
            st.error(f"An error occurred during transcription: {e}")
        return None

# Analyze sentiment of text
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    # Adjusted thresholds for polarity
    if polarity > 0.1:  # Lower the positive threshold for milder positivity
        return "Positive"
    elif polarity < -0.1:  # Lower the negative threshold to avoid false negatives
        return "Negative"
    else:
        # For very neutral text, use subjectivity to decide
        if subjectivity < 0.3:  # Highly objective text is usually neutral
            return "Neutral"
        else:
            return "Mixed"


# Save results to Excel
def save_results_to_excel(data):
    today_date = datetime.now().strftime("%m_%d_%y")
    results_filename = f"Results_of_{today_date}.xlsx"
    
    if os.path.exists(results_filename):
        existing_data = pd.read_excel(results_filename)
        new_data = pd.concat([existing_data, pd.DataFrame(data)], ignore_index=True)
    else:
        new_data = pd.DataFrame(data)
    
    new_data.to_excel(results_filename, index=False)
    return results_filename

# Save results to text file
def save_results_to_text(data):
    today_date = datetime.now().strftime("%m_%d_%y")
    results_filename = f"Results_of_{today_date}.txt"
    
    with open(results_filename, 'w') as file:
        for entry in data:
            file.write(f"Audio File Name: {entry['Audio File Name']}\n")
            file.write(f"Transcript/Translation: {entry['Transcript/Translation']}\n")
            file.write(f"Format Chosen: {entry['Format Chosen']}\n")
            file.write(f"Sentiment: {entry['Sentiment']}\n")
            file.write("\n" + "-"*50 + "\n\n")
    
    return results_filename

# Main Streamlit app
def main():
    st.title("⏯Audio Transcription📝 and Translation▶")

    # Add sidebar
    with st.sidebar:
        st.header("About 📆")
        st.write("This tool lets you upload your audio file(s) and select between transcription or translation. The results are saved in an Excel file.")
        st.header("Developed By")
        st.write("NICTU, LBSNAA for educational and learning purpose")
        st.image("https://www.lbsnaa.gov.in/admin_assets/images/logo.png")
        st.header("Share Feedback on")
        st.write("nictu@lbsnaa.gov.in")

    audio_files = st.file_uploader("Upload audio files", accept_multiple_files=True, type=["wav", "mp3", "flac"])

    if audio_files:
        format_options = ["Conversation style, accurately identify speakers", "Paragraph", "Bullet points", "Summary"]
        selected_format = st.selectbox("Choose output format", format_options)

        option = st.selectbox("Choose an option", ["Transcribe", "Translate"])

        if st.button("Process"):
            results_data = []
            progress_bar = st.progress(0)

            for idx, audio_file in enumerate(audio_files):
                try:
                    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                        temp_file.write(audio_file.read())
                        audio_path = temp_file.name

                    if option == "Transcribe":
                        result_text = transcribe(audio_path, selected_format)
                    elif option == "Translate":
                        result_text = translate(audio_path, selected_format)

                    sentiment = analyze_sentiment(result_text)

                    results_data.append({
                        "Audio File Name": audio_file.name,
                        "Transcript/Translation": result_text,
                        "Format Chosen": selected_format,
                        "Sentiment": sentiment
                    })

                    progress_bar.progress(int(((idx + 1) / len(audio_files)) * 100))

                except Exception as e:
                    st.error(f"An error occurred with file {audio_file.name}: {e}")

            # Save all results to Excel and text file
            if results_data:
                saved_excel_file = save_results_to_excel(results_data)
                saved_text_file = save_results_to_text(results_data)
                
                st.success(f"Results saved to {saved_excel_file} and {saved_text_file}")

                with open(saved_excel_file, "rb") as file:
                    st.download_button("Download Excel Results", file, file_name=saved_excel_file)
                
                with open(saved_text_file, "rb") as file:
                    st.download_button("Download Text Results", file, file_name=saved_text_file)

if __name__ == "__main__":
    main()

# import streamlit as st
# import os
# from typing import List, Dict, Optional
# from concurrent.futures import ThreadPoolExecutor
# from config import SUPPORTED_AUDIO_FORMATS, FORMAT_OPTIONS, MODEL_NAME
# from utils.audio_processing import transcribe, translate
# from utils.sentiment_analysis import analyze_sentiment
# from utils.file_utils import save_results_to_excel, save_results_to_text
# import google.generativeai as genai
# import tempfile
# import logging

# logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# # Initialize model
# genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
# model = genai.GenerativeModel(MODEL_NAME)

# def process_audio_file(audio_file, option: str, selected_format: str) -> Dict:
#     """Process a single audio file for transcription or translation."""
#     with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_file:
#         temp_file.write(audio_file.read())
#         temp_file.flush()
#         audio_path = temp_file.name

#         result_text = transcribe(audio_path, selected_format) if option == "Transcribe" else translate(audio_path, selected_format)
#         sentiment = analyze_sentiment(result_text) if result_text else "N/A"
    
#     return {
#         "Audio File Name": audio_file.name,
#         "Transcript/Translation": result_text or "Error",
#         "Format Chosen": selected_format,
#         "Sentiment": sentiment
#     }

# def main():
#     st.title("⏯ Audio Transcription 📝 and Translation ▶")
    
#     # Sidebar
#     with st.sidebar:
#         st.header("About 📆")
#         st.write("Upload audio files for transcription or translation. Results are saved in Excel and text formats.")
#         st.header("Developed By")
#         st.write("NICTU, LBSNAA for educational purposes")
#         st.image("https://www.lbsnaa.gov.in/admin_assets/images/logo.png")
#         st.header("Share Feedback")
#         st.write("nictu@lbsnaa.gov.in")

#     audio_files = st.file_uploader("Upload audio files", accept_multiple_files=True, type=SUPPORTED_AUDIO_FORMATS)
#     if not audio_files:
#         return

#     selected_format = st.selectbox("Choose output format", FORMAT_OPTIONS)
#     option = st.selectbox("Choose an option", ["Transcribe", "Translate"])

#     if st.button("Process"):
#         status_placeholder = st.empty()
#         progress_bar = st.progress(0)
#         results_data = []

#         with ThreadPoolExecutor() as executor:
#             for idx, result in enumerate(executor.map(
#                 lambda f: process_audio_file(f, option, selected_format),
#                 audio_files
#             )):
#                 results_data.append(result)
#                 status_placeholder.text(f"Processed {result['Audio File Name']} ({idx + 1}/{len(audio_files)})")
#                 progress_bar.progress(int(((idx + 1) / len(audio_files)) * 100))

#         status_placeholder.text("Processing complete!")
        
#         # Display results
#         st.subheader("Results Preview")
#         st.dataframe(pd.DataFrame(results_data))

#         # Save results
#         saved_excel_file = save_results_to_excel(results_data)
#         saved_text_file = save_results_to_text(results_data)
        
#         st.success(f"Results saved to {saved_excel_file} and {saved_text_file}")
        
#         with open(saved_excel_file, "rb") as file:
#             st.download_button("Download Excel Results", file, file_name=saved_excel_file)
#         with open(saved_text_file, "rb") as file:
#             st.download_button("Download Text Results", file, file_name=saved_text_file)

# if __name__ == "__main__":
#     if not os.environ.get("GOOGLE_API_KEY"):
#         st.error("Google API key not found. Please set the GOOGLE_API_KEY environment variable.")
#     else:
#         main()
