from flask import Blueprint, jsonify, request
from services.gemini_service import generate_quiz
from services.db_service import db_service
import json

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/', methods=['GET'])
def get_quiz():
    quiz_json_str = generate_quiz()
    try:
        quiz_data = json.loads(quiz_json_str)
        return jsonify(quiz_data), 200
    except Exception as e:
        print(f"Failed to parse quiz JSON: {e}, string was: {quiz_json_str}")
        return jsonify({"error": "Failed to generate valid quiz"}), 500

@quiz_bp.route('/score', methods=['POST'])
def save_score():
    data = request.get_json()
    if not data or 'email' not in data or 'score' not in data or 'total' not in data:
        return jsonify({"error": "Missing required fields"}), 400
        
    email = data['email']
    score = int(data['score'])
    total = int(data['total'])
    
    db_service.save_quiz_score(email, score, total)
    return jsonify({"message": "Score saved successfully"}), 200
