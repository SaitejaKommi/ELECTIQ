from flask import Blueprint, jsonify
from backend.services.search_service import fetch_election_news
from backend.utils.cache import cache

news_bp = Blueprint('news', __name__)

@news_bp.route('/', methods=['GET'])
@cache.cached(timeout=600) # Cache for 10 minutes
def get_news():
    articles = fetch_election_news()
    return jsonify(articles), 200
