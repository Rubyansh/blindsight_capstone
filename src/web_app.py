"""
Flask web application for Blind Vision Assistant
CBSE AI Capstone Project 2025
"""

import os
import asyncio
import logging
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object('config')

# Import after config is set
from src.vision_ai import get_image_description
from src.tts_engine import generate_speech
from src.utils import allowed_file, secure_filename_with_timestamp

@app.route('/', methods=['GET', 'POST'])
async def index():
    """Main route - handles both GET and POST requests"""
    if request.method == 'GET':
        return render_template('index.html')
    
    # Handle POST request (file upload)
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed. Please upload an image.'}), 400
    
    try:
        # Save uploaded file with secure filename
        filename = secure_filename_with_timestamp(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        logger.info(f"File uploaded and saved: {filename}")
        
        # Generate description using AI
        description = get_image_description(filepath)
        
        # Generate TTS audio
        audio_filename = await generate_speech(description)
        
        if not audio_filename:
            return jsonify({'error': 'Failed to generate audio'}), 500
        
        # Return results
        return render_template('index.html', 
                             description=description, 
                             image=f'uploads/{filename}',
                             audio=os.path.basename(audio_filename))
    
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        return jsonify({'error': 'Error processing image. Please try again.'}), 500

@app.route('/audio/<filename>')
def download_audio(filename):
    """Serve audio files for download"""
    try:
        audio_path = os.path.join(app.config['AUDIO_FOLDER'], filename)
        if not os.path.exists(audio_path):
            return jsonify({'error': 'Audio file not found'}), 404
        
        return send_file(audio_path, as_attachment=True)
    
    except Exception as e:
        logger.error(f"Error serving audio file: {e}")
        return jsonify({'error': 'Error serving audio file'}), 500

@app.route('/api/describe', methods=['POST'])
async def api_describe():
    """API endpoint for image description"""
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename_with_timestamp(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Generate description
        description = get_image_description(filepath)
        
        # Generate TTS
        audio_filename = await generate_speech(description)
        
        return jsonify({
            'success': True,
            'description': description,
            'image_url': f'/static/uploads/{filename}',
            'audio_url': f'/audio/{os.path.basename(audio_filename)}' if audio_filename else None
        })
    
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)