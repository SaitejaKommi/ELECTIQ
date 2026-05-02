"""
Search route for the ElectIQ backend.
Provides search results using Google Custom Search API.
"""
from flask import Blueprint, request, jsonify
from backend.services.search_service import search_election_topics
from backend.utils.rate_limiter import limiter
from backend.utils.sanitizer import sanitize_input
from backend.utils.constants import MAX_INPUT_LENGTH
from backend.utils.cache import cache

search_bp = Blueprint('search', __name__)

@search_bp.route('/', methods=['GET'])
@limiter.limit("20 per minute")
@cache.cached(timeout=600, query_string=True)
def search_endpoint() -> tuple[dict, int]:
    """
    Endpoint to search for election topics.
    
    Returns:
        JSON response with a list of search results.
    """
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "Missing 'q' parameter"}), 400
        
    query = sanitize_input(query)
    
    if len(query) > MAX_INPUT_LENGTH:
        return jsonify({"error": "Query is too long"}), 400
        
    results = search_election_topics(query)
    return jsonify({"results": results}), 200
