"""
Constants for ElectIQ backend.
Contains all hardcoded values: rate limits, cache durations, max input lengths,
API model names, and supported languages.
"""

# Cache configurations
CACHE_DEFAULT_TIMEOUT: int = 600  # 10 minutes
QUIZ_CACHE_TIMEOUT: int = 300     # 5 minutes
NEWS_CACHE_TIMEOUT: int = 600     # 10 minutes
FACT_CACHE_TIMEOUT: int = 86400   # 24 hours
GLOSSARY_CACHE_TIMEOUT: int = 86400 # 24 hours
SEARCH_CACHE_TIMEOUT: int = 600   # 10 minutes

# Security & Rate Limiting
MAX_INPUT_LENGTH: int = 1000
MAX_CONTENT_LENGTH: int = 2048  # 2KB absolute max for requests
DEFAULT_RATE_LIMIT: str = "100 per day"
API_RATE_LIMIT: str = "20 per minute"

# Gemini Config
GEMINI_MODEL_CHAT: str = 'gemini-2.5-flash'
GEMINI_MODEL_QUIZ: str = 'gemini-2.5-flash'
GEMINI_MODEL_FACT: str = 'gemini-2.5-flash'
GEMINI_MODEL_GLOSSARY: str = 'gemini-2.5-flash'

# Supported languages
SUPPORTED_LANGUAGES: list[str] = ['en', 'hi', 'es', 'fr', 'te']
