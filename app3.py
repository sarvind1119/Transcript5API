import streamlit as st
import google.generativeai as genai
import tempfile
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from textblob import TextBlob
import mimetypes

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# ---------------------------- Utility Functions ---------------------------- #

def analyze_sentiment(text):
    """Analyze sentiment using TextBlob."""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral" if subjectivity < 0.3 else "Mixed"


def save_results_to_excel(data):
    """Save results to an Excel file."""
    today_date = datetime.now().strftime("%m_%d_%y")
    results_filename = f"Results_of_{today_date}.xlsx"

    if os.path.exists(results_filename):
        existing_data = pd.read_excel(results_filename)
        new_data = pd.concat([existing_data, pd.DataFrame(data)], ignore_index=True)
    else:
        new_data = pd.DataFrame(data)

    new_data.to_excel(results_filename, index=False)
    return results_filename


def save_results_to_text(data):
    """Save results to a text file."""
    today_date = datetime.now().strftime("%m_%d_%y")
    results_filename = f"Results_of_{today_date}.txt"

    with open(results_filename, "w", encoding="utf-8") as file:
        for entry in data:
            file.write(f"Audio File Name: {entry['Audio File Name']}\n")
            file.write(f"Transcript/Translation: {entry['Transcript/Translation']}\n")
            file.write(f"Format Chosen: {entry['Format Chosen']}\n")
            file.write(f"Sentiment: {entry['Sentiment']}\n")
            file.write("\n" + "-" * 60 + "\n\n")

    return results_filename


def process_audio(audio_path, format_type, option):
    """Transcribe or translate the given audio file."""
    try:
        # Detect MIME type
        mime_type, _ = mimetypes.guess_type(audio_path)
        if not mime_type:
            mime_type = "audio/wav"

        with open(audio_path, "rb") as f:
            audio_bytes = f.read()

        if option == "Transcribe":
            prompt = f"Act as a speech recognition expert. Provide a complete transcript in {format_type} format."
        else:
            prompt = f"Translate the following audio to English in {format_type} format."

        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(
            [
                prompt,
                {"mime_type": mime_type, "data": audio_bytes}
            ]
        )

        return response.text.strip() if response.text else "No output generated."

    except Exception as e:
        st.error(f"Error processing {os.path.basename(audio_path)}: {e}")
        return None


# ---------------------------- Streamlit UI ---------------------------- #

def main():
    st.set_page_config(page_title="Audio Transcription & Translation", page_icon="🎧", layout="wide")
    st.title("🎧 Audio Transcription 📝 & Translation ▶️")

    # Sidebar Information
    with st.sidebar:
        st.header("About 📖")
        st.write("Upload one or more audio files to transcribe or translate them automatically using Gemini 1.5 Flash.")
        st.write("Results are analyzed for sentiment and saved to Excel and text files.")
        st.divider()
        st.header("Developed by 💻")
        st.write("**NICTU, LBSNAA** — for educational and learning purposes.")
        st.image("https://www.lbsnaa.gov.in/admin_assets/images/logo.png", use_container_width=True)
        st.header("📩 Feedback")
        st.write("nictu@lbsnaa.gov.in")

    audio_files = st.file_uploader(
        "Upload one or more audio files",
        accept_multiple_files=True,
        type=["wav", "mp3", "flac", "ogg", "m4a"]
    )

    if audio_files:
        format_options = [
            "Conversation style (identify speakers)",
            "Paragraph",
            "Bullet points",
            "Summary"
        ]
        selected_format = st.selectbox("Choose output format:", format_options)
        option = st.radio("Choose task:", ["Transcribe", "Translate"], horizontal=True)

        if st.button("🚀 Process All Files"):
            results_data = []
            progress_bar = st.progress(0)
            status_text = st.empty()

            for idx, audio_file in enumerate(audio_files):
                try:
                    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                        tmp.write(audio_file.read())
                        audio_path = tmp.name

                    status_text.text(f"Processing {audio_file.name} ...")
                    result_text = process_audio(audio_path, selected_format, option)

                    if result_text:
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

            status_text.text("✅ Processing complete!")

            # Save Results
            if results_data:
                saved_excel = save_results_to_excel(results_data)
                saved_text = save_results_to_text(results_data)

                st.success(f"Results saved to `{saved_excel}` and `{saved_text}`.")

                col1, col2 = st.columns(2)
                with col1:
                    with open(saved_excel, "rb") as f:
                        st.download_button("📊 Download Excel Results", f, file_name=saved_excel)
                with col2:
                    with open(saved_text, "rb") as f:
                        st.download_button("📄 Download Text Results", f, file_name=saved_text)


if __name__ == "__main__":
    main()
