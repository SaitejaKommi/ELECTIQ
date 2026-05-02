"""
Main application module for the ElectIQ backend.
Initializes Flask, sets up security, registers blueprints, and handles global errors.
"""
import os
import logging
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from flask_talisman import Talisman

# Import config
from backend.config import get_config

# Import routes and utilities
from backend.routes.chat import chat_bp
from backend.routes.quiz import quiz_bp
from backend.routes.news import news_bp
from backend.routes.translate import translate_bp
from backend.routes.auth import auth_bp
from backend.routes.fact import fact_bp
from backend.routes.glossary import glossary_bp
from backend.routes.search import search_bp
from backend.routes.tts import tts_bp
from backend.utils.rate_limiter import limiter
from backend.utils.cache import cache
from backend.utils.constants import CACHE_DEFAULT_TIMEOUT, MAX_CONTENT_LENGTH

def create_app(test_config: dict | None = None) -> Flask:
    """
    Application factory for the ElectIQ Flask backend.
    
    Initializes Flask, sets up security headers via Talisman,
    configures strict CORS, registers blueprints, and sets up
    global error handling and input validation.
    
    Args:
        test_config (dict | None, optional): Configuration for testing.
        
    Returns:
        Flask: The initialized Flask application.
    """
    app = Flask(__name__, static_folder="../frontend")
    config = get_config()
    
    if test_config:
        app.config.update(test_config)
    else:
        app.config['SECRET_KEY'] = config.SECRET_KEY
        app.config['CACHE_TYPE'] = config.CACHE_TYPE
        app.config['CACHE_DEFAULT_TIMEOUT'] = CACHE_DEFAULT_TIMEOUT
        app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
        
    # Strictly limit CORS to Vercel and local dev
    CORS(app, resources={r"/api/*": {"origins": [r"^https://.*\.vercel\.app$", r"^http://localhost:\d+$"]}})
    
    # Initialize Extensions
    limiter.init_app(app)
    cache.init_app(app)
    
    # Content Security Policy and Security Headers
    csp = {
        'default-src': ["'self'", 'https://fonts.googleapis.com', 'https://fonts.gstatic.com', 'data:', 'blob:'],
        'script-src': ["'self'", "'unsafe-inline'", "https://www.googletagmanager.com"],
        'style-src': ["'self'", "'unsafe-inline'", 'https://fonts.googleapis.com'],
        'img-src': ["'self'", 'data:', 'https:'],
        'connect-src': ["'self'", "https://www.google-analytics.com", "https://analytics.google.com"]
    }
    
    Talisman(
        app, 
        content_security_policy=csp, 
        force_https=False,
        strict_transport_security=True,
        frame_options='DENY',
        referrer_policy='strict-origin-when-cross-origin'
    )

    # Global request validation
    @app.before_request
    def validate_request_length():
        """Ensure no request exceeds the maximum allowed content length."""
        if request.content_length and request.content_length > MAX_CONTENT_LENGTH:
            return jsonify({"error": "Payload too large"}), 413

    # Global Error Handlers (Prevents stack traces)
    @app.errorhandler(404)
    def not_found_error(error) -> tuple[dict, int]:
        """Handles 404 Not Found errors globally."""
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error) -> tuple[dict, int]:
        """Handles 500 Internal Server errors globally."""
        logging.error(f"Server Error: {error}")
        return jsonify({"error": "Internal server error"}), 500

    @app.errorhandler(Exception)
    def handle_exception(e: Exception) -> tuple[dict, int]:
        """Handles all unhandled exceptions globally to prevent stack trace leaks."""
        logging.error(f"Unhandled Exception: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(quiz_bp, url_prefix='/api/quiz')
    app.register_blueprint(news_bp, url_prefix='/api/news')
    app.register_blueprint(translate_bp, url_prefix='/api/translate')
    app.register_blueprint(fact_bp, url_prefix='/api/fact')
    app.register_blueprint(glossary_bp, url_prefix='/api/glossary')
    app.register_blueprint(search_bp, url_prefix='/api/search')
    app.register_blueprint(tts_bp, url_prefix='/api/tts')
    
    # Health check
    @app.route('/api/health')
    def health_check():
        """Health check endpoint."""
        return jsonify({"status": "healthy"}), 200

    # Serve Frontend SPA
    @app.route('/')
    def index():
        """Serve the main frontend application."""
        return send_from_directory(app.static_folder, 'index.html')
        
    @app.route('/<path:path>')
    def serve_static(path: str):
        """Serve static files or fallback to index.html for SPA routing."""
        if os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, 'index.html')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=False)
