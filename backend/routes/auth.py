"""
Auth routing module for the ElectIQ backend.
Handles basic email-based user tracking.
"""
from flask import Blueprint, request, jsonify
from backend.services.db_service import db_service
from backend.utils.sanitizer import sanitize_input, is_valid_email
from backend.utils.rate_limiter import limiter

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("50 per minute")
def login():
    """
    Handle POST requests for user login/registration.
    
    Validates and sanitizes email input. Creates a user record
    if one does not exist, or fetches the existing user.
    
    Returns:
        Response: JSON object with login success and history count.
    """
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({"error": "Email is required"}), 400
        
    email = sanitize_input(str(data.get('email', ''))[:1000])
    if not is_valid_email(email):
        return jsonify({"error": "Invalid email format"}), 400
        
    user = db_service.get_or_create_user(email)
    
    return jsonify({
        "message": "Login successful",
        "email": user["email"],
        "history_count": len(user.get("chat_history", []))
    }), 200
