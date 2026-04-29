# 🌸 Bloom Notes — AI Meeting Summarizer

A fully local + free AI meeting summarizer using:
- **faster-whisper** — local Whisper transcription (no API key)
- **Groq API** — free LLM summarization (free tier, no credit card)
- **ReportLab** — PDF export (local, free)
- **Flask** — lightweight Python web server

---

## ⚙️ Setup (Python 3.11 recommended)

### 1. Get a FREE Groq API Key
1. Go to https://console.groq.com
2. Sign up (free, no credit card required)
3. Go to API Keys → Create API Key
4. Copy the key (starts with `gsk_...`)

### 2. Create & activate a virtual environment
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

> **Note:** `faster-whisper` will download the Whisper `base` model (~150MB) on first run automatically.

### 4. Set your Groq API key

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="gsk_your_key_here"
```

**Windows (CMD):**
```cmd
set GROQ_API_KEY=gsk_your_key_here
```

**Mac/Linux:**
```bash
export GROQ_API_KEY=gsk_your_key_here
```

### 5. Run the app
```bash
python app.py
```

Open your browser at: **http://localhost:5000**

---

## 🎯 Usage
1. Enter meeting title, date, and participant names
2. Upload your audio file (MP3, WAV, M4A, OGG, FLAC, etc.)
3. Click **Upload & Start** — transcription and summarization run automatically
4. View your structured meeting notes with action items, decisions, and follow-ups
5. Click **Export PDF** to download professional meeting minutes

---

## 🔧 Whisper Model Options
Edit `transcriber.py` to change the model:
| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| `tiny` | 75MB | Fastest | Lower |
| `base` | 150MB | Fast | Good (default) |
| `small` | 490MB | Medium | Better |
| `medium` | 1.5GB | Slow | Great |
| `large-v3` | 3GB | Slowest | Best |

---

## 📦 Tech Stack (All Free)
- `faster-whisper` — CTranslate2-based Whisper, runs on CPU
- `groq` — Groq SDK (free tier: 14,400 requests/day)
- `flask` — Web framework
- `reportlab` — PDF generation
