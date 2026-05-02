import requests

def translate_text(text: str, target_language: str) -> str:
    """Translates text to the target language using MyMemory API."""
    if not text or target_language == 'en':
        return text
        
    url = "https://api.mymemory.translated.net/get"
    params = {
        "q": text,
        "langpair": f"en|{target_language}"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data and data.get("responseData") and data["responseData"].get("translatedText"):
            return data["responseData"]["translatedText"]
        return text
    except Exception as e:
        print(f"Translation error: {e}")
        return text
