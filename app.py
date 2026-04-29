import os
import json
import uuid
import time
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

ALLOWED_EXTENSIONS = {'mp3', 'mp4', 'wav', 'ogg', 'm4a', 'flac', 'webm'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    file = request.files['audio']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not supported'}), 400

    job_id = str(uuid.uuid4())
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{job_id}_{filename}")
    file.save(filepath)

    return jsonify({'job_id': job_id, 'filename': filename, 'filepath': filepath})

@app.route('/transcribe', methods=['POST'])
def transcribe():
    data = request.json
    job_id = data.get('job_id')
    filepath = data.get('filepath')

    if not filepath or not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    try:
        from transcriber import transcribe_audio
        transcript = transcribe_audio(filepath)
        return jsonify({'job_id': job_id, 'transcript': transcript})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    transcript = data.get('transcript', '')
    meeting_title = data.get('meeting_title', 'Meeting')
    meeting_date = data.get('meeting_date', '')
    participants = data.get('participants', '')

    if not transcript:
        return jsonify({'error': 'No transcript provided'}), 400

    try:
        from summarizer import analyze_meeting
        result = analyze_meeting(transcript, meeting_title, meeting_date, participants)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export_pdf', methods=['POST'])
def export_pdf():
    data = request.json
    try:
        from pdf_exporter import generate_pdf
        job_id = str(uuid.uuid4())
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"meeting_minutes_{job_id}.pdf")
        generate_pdf(data, output_path)
        return send_file(output_path, as_attachment=True, download_name='meeting_minutes.pdf')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    app.run(debug=True, port=5000)
