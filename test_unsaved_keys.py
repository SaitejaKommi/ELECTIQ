import os

# Set environment variables from user's active document manually
os.environ["MONGODB_URI"] = r"mongodb+srv://sai24bcs10337_db_user:cgy5MZyXkPdap5er@cluster0.ggvi5ta.mongodb.net/"
os.environ["GEMINI_API_KEY"] = "AIzaSyDOd0dDXvo4tFZOOsK81Vgcyw0XvRXWi1s"
os.environ["GOOGLE_SEARCH_API_KEY"] = "AIzaSyBjckpcthnVphqGbOZre-k3_UQJf-jmscM"
os.environ["GOOGLE_SEARCH_ENGINE_ID"] = "c72006a17b6e2436d"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\kommi\Downloads\ELECTIQ\ellectq-5f90fc0e322f.json"

errors = []

# 1. Check MongoDB
try:
    from pymongo import MongoClient
    client = MongoClient(os.environ["MONGODB_URI"], serverSelectionTimeoutMS=5000)
    client.server_info()
    print("[OK] MongoDB")
except Exception as e:
    errors.append(f"[FAIL] MongoDB: {e}")

# 2. Check Gemini
try:
    import google.generativeai as genai
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Hello")
    if response.text:
        print("[OK] Gemini")
    else:
        errors.append("[FAIL] Gemini: Empty response")
except Exception as e:
    errors.append(f"[FAIL] Gemini: {e}")

# 3. Check Google Custom Search
try:
    import requests
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": os.environ["GOOGLE_SEARCH_API_KEY"], "cx": os.environ["GOOGLE_SEARCH_ENGINE_ID"], "q": "test", "num": 1}
    res = requests.get(url, params=params)
    res.raise_for_status()
    print("[OK] Search")
except Exception as e:
    errors.append(f"[FAIL] Search: {e}")

# 4. Check Google Translate
try:
    from google.cloud import translate_v2 as translate
    translate_client = translate.Client()
    result = translate_client.translate("Hello", target_language="es")
    if result and "translatedText" in result:
        print("[OK] Translate")
except Exception as e:
    errors.append(f"[FAIL] Translate: {e}")

# 5. Check Google TTS
try:
    from google.cloud import texttospeech
    tts_client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text="Hello")
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    if response.audio_content:
        print("[OK] TTS")
except Exception as e:
    errors.append(f"[FAIL] TTS: {e}")

print("ERRORS:", errors)
