"""
Translation service module for the ElectIQ backend.
Handles translation of text via Google Cloud Translate API with fallback to MyMemory API.
"""
import logging
import requests
from google.cloud import translate_v2 as translate
from backend.config import get_config

config = get_config()

def _translate_google(text: str, target_language: str) -> str:
    """Translates text using Google Cloud Translate API."""
    # This requires GOOGLE_APPLICATION_CREDENTIALS to be set
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

def _translate_mymemory(text: str, target_language: str) -> str:
    """Translates text using MyMemory API (Fallback)."""
    url = "https://api.mymemory.translated.net/get"
    params = {
        "q": text,
        "langpair": f"en|{target_language}"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    if data and data.get("responseData") and data["responseData"].get("translatedText"):
        return data["responseData"]["translatedText"]
    return text

def translate_text(text: str, target_language: str) -> str:
    """
    Translates text to the target language.
    Attempts Google Cloud Translate first, falls back to MyMemory API on failure.
    
    Args:
        text (str): Text to translate.
        target_language (str): Target language code (e.g., 'es').
        
    Returns:
        str: Translated text or original text on failure.
    """
    if not text or target_language == 'en':
        return text
        
    try:
        # Check if Google credentials exist
        if config.GOOGLE_APPLICATION_CREDENTIALS:
            return _translate_google(text, target_language)
        else:
            logging.warning("Google credentials not found. Falling back to MyMemory translate.")
            return _translate_mymemory(text, target_language)
    except Exception as e:
        logging.error(f"Google Translate failed: {e}. Falling back to MyMemory.")
        try:
            return _translate_mymemory(text, target_language)
        except Exception as e2:
            logging.error(f"MyMemory Translate failed: {e2}")
            return text
