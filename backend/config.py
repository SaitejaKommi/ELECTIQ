"""
Configuration module for ElectIQ backend.
Centralizes all environment variable loading.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

class Config:
    """Base configuration class."""
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-key-please-change')
    GEMINI_API_KEY: str | None = os.getenv('GEMINI_API_KEY')
    MONGODB_URI: str | None = os.getenv('MONGODB_URI')
    
    # Google Services Keys
    GOOGLE_APPLICATION_CREDENTIALS: str | None = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    GOOGLE_SEARCH_API_KEY: str | None = os.getenv('GOOGLE_SEARCH_API_KEY')
    GOOGLE_SEARCH_CX: str | None = os.getenv('GOOGLE_SEARCH_CX')
    
    # Firebase
    FIREBASE_CREDENTIALS_PATH: str | None = os.getenv('FIREBASE_CREDENTIALS_PATH')
    
    # Flask settings
    CACHE_TYPE: str = 'SimpleCache'

def get_config() -> Config:
    """
    Returns the loaded configuration.
    
    Returns:
        Config: The application configuration object.
    """
    return Config()
