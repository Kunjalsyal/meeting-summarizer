"""
Transcription using faster-whisper — fully local, no API key needed.
Model: 'base' by default (fast + decent quality).
Upgrade to 'small', 'medium', or 'large-v3' for better accuracy.
"""

from faster_whisper import WhisperModel

_model = None

def get_model():
    global _model
    if _model is None:
        print("Loading Whisper model (base)... This may take a moment on first run.")
        _model = WhisperModel("base", device="cpu", compute_type="int8")
    return _model

def transcribe_audio(filepath: str) -> str:
    model = get_model()
    segments, info = model.transcribe(filepath, beam_size=5)
    
    print(f"Detected language: {info.language} (probability: {info.language_probability:.2f})")
    
    full_text = []
    for segment in segments:
        full_text.append(segment.text.strip())
    
    return " ".join(full_text)
