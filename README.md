````markdown
---

## 🌸 Bloom Notes  
**AI-powered meeting summarizer that runs locally — no subscriptions, no BS**

Turn raw meeting audio into clean, structured notes with action items, decisions, and summaries — without sending your data to random servers.

---

## 🚀 What this actually does
- Upload a meeting recording  
- Generate a full transcript (runs locally using Whisper)  
- Convert it into structured notes using an LLM  
- Export clean meeting minutes as a PDF  

---

## 🧠 Why this exists
Most meeting tools:
- Hide useful features behind paywalls  
- Depend heavily on cloud APIs  
- Or store sensitive data externally  

Bloom Notes is built to be:
- Local-first  
- Free to use  
- Simple and practical  

---

## ⚡ Tech Stack
- faster-whisper (local transcription)
- Groq API (LLM summarization)
- Flask (backend)
- ReportLab (PDF generation)

---

## 🛠 Setup

### 1. Get Groq API key (free)
https://console.groq.com

---

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
````

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```
