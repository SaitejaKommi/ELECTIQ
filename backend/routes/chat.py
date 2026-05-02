"""
Chat routing module for the ElectIQ backend.
Handles AI chat interactions via Gemini API.
"""
from flask import Blueprint, request, jsonify
from backend.services.gemini_service import get_chat_response
from backend.utils.sanitizer import sanitize_input
from backend.utils.rate_limiter import limiter

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/', methods=['POST'])
@limiter.limit("20 per minute")
def chat():
    """
    Handle POST requests for AI chat interaction.
    
    Expects a JSON payload with 'email' and 'message'.
    Sanitizes inputs and fetches AI response.
    
    Returns:
        Response: JSON object containing AI response or error message.
    """
    data = request.get_json()
    if not data or 'message' not in data or 'email' not in data:
        return jsonify({"error": "Message and email are required"}), 400
        
    email = sanitize_input(str(data.get('email', ''))[:1000])
    message = sanitize_input(str(data.get('message', ''))[:1000])
    
    if not message:
        return jsonify({"error": "Message cannot be empty"}), 400
        
    response_text = get_chat_response(email, message)
    
    return jsonify({"response": response_text}), 200
