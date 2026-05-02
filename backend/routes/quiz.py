"""
Quiz routing module for the ElectIQ backend.
Handles generation of quizzes and score saving.
"""
import json
from flask import Blueprint, jsonify, request
from backend.services.gemini_service import generate_quiz
from backend.services.db_service import db_service
from backend.utils.sanitizer import sanitize_input
from backend.utils.rate_limiter import limiter
from backend.utils.cache import cache

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/', methods=['GET'])
@limiter.limit("10 per minute")
@cache.cached(timeout=300) # Cache for 5 minutes
def get_quiz():
    """
    Handle GET requests to generate a new quiz.
    
    Utilizes Gemini API to generate JSON formatted questions.
    Caches the generated quiz for 5 minutes for efficiency.
    
    Returns:
        Response: JSON array of quiz questions or error message.
    """
    quiz_json_str = generate_quiz()
    try:
        quiz_data = json.loads(quiz_json_str)
        return jsonify(quiz_data), 200
    except Exception as e:
        # Avoid exposing raw stack traces to the user
        return jsonify({"error": "Failed to generate valid quiz"}), 500

@quiz_bp.route('/score', methods=['POST'])
@limiter.limit("20 per minute")
def save_score():
    """
    Handle POST requests to save a user's quiz score.
    
    Expects a JSON payload with 'email', 'score', and 'total'.
    Sanitizes email before saving.
    
    Returns:
        Response: JSON success or error message.
    """
    data = request.get_json()
    if not data or 'email' not in data or 'score' not in data or 'total' not in data:
        return jsonify({"error": "Missing required fields"}), 400
        
    email = sanitize_input(str(data.get('email', ''))[:1000])
    try:
        score = int(data['score'])
        total = int(data['total'])
    except ValueError:
        return jsonify({"error": "Invalid score format"}), 400
    
    db_service.save_quiz_score(email, score, total)
    return jsonify({"message": "Score saved successfully"}), 200
