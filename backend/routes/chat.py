from flask import Blueprint, request, jsonify
from services.gemini_service import get_chat_response
from utils.sanitizer import sanitize_input
from utils.rate_limiter import limiter

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/', methods=['POST'])
@limiter.limit("20 per minute")
def chat():
    data = request.get_json()
    if not data or 'message' not in data or 'email' not in data:
        return jsonify({"error": "Message and email are required"}), 400
        
    email = sanitize_input(data['email'])
    message = sanitize_input(data['message'])
    
    if not message:
        return jsonify({"error": "Message cannot be empty"}), 400
        
    response_text = get_chat_response(email, message)
    
    return jsonify({"response": response_text}), 200
