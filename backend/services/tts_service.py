import base64
from google.cloud import texttospeech

_tts_client = None

def get_client():
    global _tts_client
    if _tts_client is None:
        try:
            _tts_client = texttospeech.TextToSpeechClient()
        except Exception as e:
            print(f"Failed to initialize TTS client: {e}")
    return _tts_client

def generate_speech(text: str, language_code: str = "en-US") -> str:
    """Converts text to speech and returns base64 audio content."""
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
