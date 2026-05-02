"""
Fact routing module for the ElectIQ backend.
Fetches the Election Fact of the Day via Gemini.
"""
from flask import Blueprint, jsonify
from backend.services.gemini_service import generate_fact
from backend.utils.cache import cache
from backend.utils.rate_limiter import limiter

fact_bp = Blueprint('fact', __name__)

@fact_bp.route('/', methods=['GET'])
@limiter.limit("50 per minute")
@cache.cached(timeout=86400) # Cache for 24 hours (Fact of the day)
def get_fact():
    """
    Handle GET requests to fetch the Election Fact of the Day.
    
    Caches the fact for 24 hours.
    
    Returns:
        Response: JSON object containing the fact.
    """
    fact = generate_fact()
    return jsonify({"fact": fact}), 200
