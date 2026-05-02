"""
Constants for ElectIQ backend.
"""
import os

# Cache configurations
CACHE_DEFAULT_TIMEOUT = 600  # 10 minutes
QUIZ_CACHE_TIMEOUT = 300     # 5 minutes
NEWS_CACHE_TIMEOUT = 600     # 10 minutes

# Security & Rate Limiting
MAX_INPUT_LENGTH = 1000
MAX_CONTENT_LENGTH = 2048  # 2KB absolute max for requests
DEFAULT_RATE_LIMIT = "100 per day"
API_RATE_LIMIT = "20 per minute"

# Gemini Config
GEMINI_MODEL_CHAT = 'gemini-2.5-flash'
GEMINI_MODEL_QUIZ = 'gemini-2.5-flash'
GEMINI_MODEL_FACT = 'gemini-2.5-flash'

# Supported languages
SUPPORTED_LANGUAGES = ['en', 'hi', 'es', 'fr', 'te']
