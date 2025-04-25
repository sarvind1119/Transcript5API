
# 📘 Audio Transcription & Translation App

Developed by **NICTU, LBSNAA**, this Streamlit-based tool allows users to **transcribe** or **translate** audio files with ease. The application leverages **Google Gemini AI** for content generation and offers **sentiment analysis**, **multi-format outputs**, and **export features** for reporting.

---

## 🧩 Features

| Feature                          | Description |
|----------------------------------|-------------|
| 🎙️ Multi-Audio Upload           | Upload and process multiple audio files (MP3, WAV, FLAC) simultaneously. |
| 📝 Transcription & Translation   | Choose to transcribe the audio or translate it into English. |
| 🧠 AI-Powered Format Selection   | Output formats: Conversation Style, Paragraph, Bullet Points, Summary. |
| 📊 Sentiment Analysis           | Analyze tone (Positive, Negative, Neutral, Mixed) using TextBlob. |
| 📁 Export Options               | Save results to Excel, Text, or individual TXT files (ZIP format). |
| 📦 Batch Processing             | Automated progress tracking and batch result generation. |

---

## 🚀 How to Use

### 1. Launch App
Use the following command in your terminal:

```bash
streamlit run app3_v2.py
```

---

### 2. Upload Audio Files
- Click on the **Upload audio files** button.
- Select **MP3**, **WAV**, or **FLAC** files.
- Multiple file selection is supported.

---

### 3. Choose Output Format
Pick from:
- Conversation style (speaker identification)
- Paragraph
- Bullet points
- Summary

---

### 4. Choose Task
Select:
- **Transcribe** – Generate transcript of the original audio.
- **Translate** – Convert the audio to English in the selected format.

---

### 5. (Optional) Export Format
- Check the box to **save individual results as text files** (ZIP download).

---

### 6. Click **Process**
- The app will show a progress bar.
- When done, download buttons will appear for:
  - **Excel file**
  - **Text summary**
  - **ZIP with per-audio `.txt` files** (if selected)

---

## 📂 Output Samples

| Column Name            | Description |
|------------------------|-------------|
| Audio File Name        | Name of the uploaded audio file |
| Transcript/Translation | AI-generated output |
| Format Chosen          | Format selected by the user |
| Sentiment              | Polarity of content (Positive, Negative, Neutral, Mixed) |

---

## 🛠️ Requirements

- Python 3.8+
- `streamlit`, `google.generativeai`, `textblob`, `pandas`, `openpyxl`, `python-dotenv`

Install all dependencies:

```bash
pip install -r requirements.txt
```

`requirements.txt` content:
```txt
streamlit
google-generativeai
textblob
pandas
openpyxl
python-dotenv
```

---

## 🔐 Environment Setup

Create a `.env` file in the same directory:

```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

Make sure `.env` is added to `.gitignore` to prevent key exposure.

---

## 📬 Feedback & Support

- Developed by: **NICTU, LBSNAA**
- Feedback email: **nictu@lbsnaa.gov.in**
- Logo: ![LBSNAA Logo](https://www.lbsnaa.gov.in/images/lbsnaa-logo.png)
