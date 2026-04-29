🌸 Bloom Notes

AI-powered meeting summarizer that runs locally — no subscriptions, no BS

Turn raw meeting audio into clean, structured notes with action items, decisions, and summaries — without sending your data to external services.

🚀 What this actually does
Upload a meeting recording
Generate a full transcript (runs locally using Whisper)
Convert it into structured notes using an LLM
Export clean meeting minutes as a PDF
🧠 Why this exists

Most meeting tools:

Hide useful features behind paywalls
Depend heavily on cloud APIs
Or store sensitive data externally

Bloom Notes is built to be:

Local-first
Free to use
Simple and practical
⚡ Tech Stack
faster-whisper (local transcription)
Groq API (LLM summarization)
Flask (backend)
ReportLab (PDF generation)
🛠 Setup
1. Get Groq API key (free)

https://console.groq.com

2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

5. Set API key

Windows (CMD):

set GROQ_API_KEY=your_key

Windows (PowerShell):

$env:GROQ_API_KEY="your_key"

Mac/Linux:

export GROQ_API_KEY=your_key
5. Run the app
python app.py

Open: http://localhost:5000

🎯 Usage
Enter meeting details
Upload audio file
Start processing
View:
Summary
Action items
Decisions
Export PDF
⚙️ Whisper Models

Edit transcriber.py to change model:

Model	Speed	Accuracy
tiny	fastest	lower
base	fast	good
small	medium	better
medium	slow	high
large-v3	slowest	best
📌 Features
Local transcription (no API required)
Fast LLM summarization
Structured meeting notes
PDF export
Simple UI
🧩 Future Improvements
Speaker identification
Live transcription
UI improvements
Multi-language support
💡 Summary

Converts meeting audio into structured notes — fast, simple, and mostly local.
