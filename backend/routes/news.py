"""
News routing module for the ElectIQ backend.
Fetches the latest election news from external APIs.
"""
from flask import Blueprint, jsonify
from backend.services.search_service import fetch_election_news
from backend.utils.cache import cache
from backend.utils.rate_limiter import limiter

news_bp = Blueprint('news', __name__)

# Basic dictionary caching with timestamp as fallback if Redis isn't used
# but @cache.cached handles in-memory timeout based on Flask-Caching.
@news_bp.route('/', methods=['GET'])
@limiter.limit("30 per minute")
@cache.cached(timeout=600) # Cache for 10 minutes
def get_news():
    """
    Handle GET requests to fetch recent election news.
    
    Caches the results for 10 minutes to minimize external API calls.
    
    Returns:
        Response: JSON array of news articles.
    """
    articles = fetch_election_news()
    return jsonify(articles), 200
