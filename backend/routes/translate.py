"""
Translate routing module for the ElectIQ backend.
Handles translation of text via MyMemory API.
"""
from flask import Blueprint, request, jsonify
from backend.services.translate_service import translate_text
from backend.utils.sanitizer import sanitize_input
from backend.utils.rate_limiter import limiter

translate_bp = Blueprint('translate', __name__)

@translate_bp.route('/', methods=['POST'])
@limiter.limit("60 per minute")
def translate_endpoint():
    """
    Handle POST requests to translate text.
    
    Expects 'text' and 'target_language' in JSON payload.
    Truncates text to 1000 characters for safety.
    
    Returns:
        Response: JSON object with translatedText.
    """
    data = request.get_json()
    if not data or 'text' not in data or 'target_language' not in data:
        return jsonify({"error": "Missing required fields"}), 400
        
    text = sanitize_input(str(data.get('text', ''))[:1000])
    target_language = sanitize_input(str(data.get('target_language', ''))[:10])
    
    if not text:
        return jsonify({"error": "Text cannot be empty"}), 400
        
    translated = translate_text(text, target_language)
    return jsonify({"translatedText": translated}), 200
