"""
Glossary route for the ElectIQ backend.
Provides simple explanations of election terms using Gemini API.
"""
from flask import Blueprint, request, jsonify
from backend.services.gemini_service import generate_glossary_term
from backend.utils.rate_limiter import limiter
from backend.utils.sanitizer import sanitize_input
from backend.utils.constants import MAX_INPUT_LENGTH
from backend.services.firebase_service import save_glossary_search

glossary_bp = Blueprint('glossary', __name__)

@glossary_bp.route('/', methods=['POST'])
@limiter.limit("30 per minute")
def glossary_endpoint() -> tuple[dict, int]:
    """
    Endpoint to get a simple explanation for an election term.
    
    Returns:
        JSON response with the explanation.
    """
    data = request.get_json()
    if not data or 'term' not in data:
        return jsonify({"error": "Missing 'term' in request body"}), 400
        
    term = sanitize_input(data['term'])
    email = sanitize_input(data.get('email', 'anonymous'))
    
    if len(term) > MAX_INPUT_LENGTH:
        return jsonify({"error": "Term is too long"}), 400
        
    explanation = generate_glossary_term(term)
    
    if explanation:
        # Track usage in Firebase
        if email != 'anonymous':
            save_glossary_search(email, term)
        return jsonify({"term": term, "explanation": explanation}), 200
    else:
        return jsonify({"error": "Failed to generate explanation"}), 500
