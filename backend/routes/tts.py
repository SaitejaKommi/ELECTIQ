from flask import Blueprint, request, jsonify
from backend.services.tts_service import generate_speech

tts_bp = Blueprint('tts', __name__)

@tts_bp.route('/', methods=['POST'])
def tts_endpoint():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing text"}), 400
        
    text = data['text']
    language_code = data.get('language_code', 'en-US')
    
    audio_content = generate_speech(text, language_code)
    if not audio_content:
        return jsonify({"error": "Failed to generate speech"}), 500
        
    return jsonify({"audioContent": audio_content}), 200
