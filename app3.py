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

#             # Save all results to Excel
#             if results_data:
#                 saved_file = save_results_to_excel(results_data)
#                 st.success(f"Results saved to {saved_file}")

#                 with open(saved_file, "rb") as file:
#                     st.download_button("Download Results", file, file_name=saved_file)

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
        st.image("https://www.lbsnaa.gov.in/images/lbsnaa-logo.png")
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
