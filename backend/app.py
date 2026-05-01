import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_talisman import Talisman
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routes
from routes.chat import chat_bp
from routes.quiz import quiz_bp
from routes.news import news_bp
from routes.translate import translate_bp
from routes.auth import auth_bp
from utils.rate_limiter import limiter
from utils.cache import cache

def create_app(test_config=None):
    app = Flask(__name__, static_folder="../frontend")
    
    if test_config:
        app.config.update(test_config)
    else:
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-please-change')
        app.config['CACHE_TYPE'] = 'SimpleCache'
        app.config['CACHE_DEFAULT_TIMEOUT'] = 600
        
    # Enable CORS for Vercel and localhost
    CORS(app, resources={r"/api/*": {"origins": [r"https://.*\.vercel\.app", r"http://localhost:.*"]}})
    
    # Initialize Rate Limiter
    limiter.init_app(app)
    
    # Initialize Cache
    cache.init_app(app)
    
    # Enable Content Security Policy headers (Relaxed for development, stricter in prod)
    # Allowing inline scripts and styles for simple SPA setup if needed
    csp = {
        'default-src': [
            '\'self\'',
            'https://fonts.googleapis.com',
            'https://fonts.gstatic.com',
            'data:',
            'blob:'
        ],
        'script-src': ['\'self\'', '\'unsafe-inline\''],
        'style-src': ['\'self\'', '\'unsafe-inline\'', 'https://fonts.googleapis.com'],
        'img-src': ['\'self\'', 'data:', 'https:']
    }
    # Disable HTTPS enforcement for local dev
    Talisman(app, content_security_policy=csp, force_https=False)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(quiz_bp, url_prefix='/api/quiz')
    app.register_blueprint(news_bp, url_prefix='/api/news')
    app.register_blueprint(translate_bp, url_prefix='/api/translate')

    # Serve Frontend SPA
    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')
        
    @app.route('/<path:path>')
    def serve_static(path):
        if os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, 'index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
