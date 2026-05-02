from flask import Blueprint, request, jsonify
from backend.services.db_service import db_service
from backend.utils.sanitizer import sanitize_input, is_valid_email

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({"error": "Email is required"}), 400
        
    email = sanitize_input(data['email'])
    if not is_valid_email(email):
        return jsonify({"error": "Invalid email format"}), 400
        
    user = db_service.get_or_create_user(email)
    
    return jsonify({
        "message": "Login successful",
        "email": user["email"],
        "history_count": len(user.get("chat_history", []))
    }), 200
