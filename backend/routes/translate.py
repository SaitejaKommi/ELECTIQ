from flask import Blueprint, request, jsonify
from services.translate_service import translate_text

translate_bp = Blueprint('translate', __name__)

@translate_bp.route('/', methods=['POST'])
def translate_endpoint():
    data = request.get_json()
    if not data or 'text' not in data or 'target_language' not in data:
        return jsonify({"error": "Missing required fields"}), 400
        
    text = data['text']
    target_language = data['target_language']
    
    translated = translate_text(text, target_language)
    return jsonify({"translatedText": translated}), 200
