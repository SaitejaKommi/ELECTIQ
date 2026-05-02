"""
Text-To-Speech service module for the ElectIQ backend.
Handles generation of audio from text via Google Cloud TTS.
"""
import base64
from google.cloud import texttospeech

_tts_client = None

def get_client() -> texttospeech.TextToSpeechClient:
    """
    Get or initialize the Google Cloud TTS client securely.
    
    Returns:
        TextToSpeechClient: Initialized client or None on failure.
    """
    global _tts_client
    if _tts_client is None:
        try:
            _tts_client = texttospeech.TextToSpeechClient()
        except Exception as e:
            print(f"Failed to initialize TTS client: {e}")
    return _tts_client

def generate_speech(text: str, language_code: str = "en-US") -> str:
    """
    Converts text to speech and returns base64 audio content.
    
    Args:
        text (str): Text to convert to speech.
        language_code (str): Language code (e.g., 'en-US').
        
    Returns:
        str: Base64 encoded audio string or empty string on failure.
    """
    client = get_client()
    if not client:
        return ""
        
    try:
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        # Select voice based on language code
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        
        # Return base64 encoded audio string
        return base64.b64encode(response.audio_content).decode('utf-8')
    except Exception as e:
        print(f"TTS error: {e}")
        return ""
