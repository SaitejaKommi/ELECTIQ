import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("--- Starting Environment Verification ---")

errors = []

# 1. Check MongoDB
try:
    print("Testing MongoDB...")
    from pymongo import MongoClient
    uri = os.getenv("MONGODB_URI")
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.server_info() # Will throw exception if cannot connect
    print("[OK] MongoDB connection successful.")
except Exception as e:
    errors.append(f"[FAIL] MongoDB connection failed: {e}")

# 2. Check Gemini
try:
    print("Testing Gemini API...")
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content("Hello")
    if response.text:
        print("[OK] Gemini API connection successful.")
    else:
        errors.append("[FAIL] Gemini API returned empty response.")
except Exception as e:
    errors.append(f"[FAIL] Gemini API connection failed: {e}")

# 3. Check NewsAPI
try:
    print("Testing NewsAPI...")
    import requests
    api_key = os.getenv("NEWS_API_KEY")
    url = "https://newsapi.org/v2/everything"
    params = {"q": "election", "apiKey": api_key, "pageSize": 1}
    headers = {"User-Agent": "ElectIQ/1.0"}
    res = requests.get(url, params=params, headers=headers)
    res.raise_for_status()
    print("[OK] NewsAPI connection successful.")
except Exception as e:
    errors.append(f"[FAIL] NewsAPI connection failed: {e}")

# 4. Check MyMemory Translate (Free, no key)
try:
    print("Testing MyMemory Translate API...")
    import requests
    url = "https://api.mymemory.translated.net/get"
    params = {"q": "Hello", "langpair": "en|es"}
    res = requests.get(url, params=params)
    res.raise_for_status()
    if res.json().get("responseData", {}).get("translatedText"):
        print("[OK] MyMemory Translate API successful.")
    else:
        errors.append("[FAIL] MyMemory Translate API invalid response.")
except Exception as e:
    errors.append(f"[FAIL] MyMemory Translate API failed: {e}")

print("\n--- Verification Summary ---")
if errors:
    print("The following issues were found:")
    for err in errors:
        print(err)
else:
    print("All environment variables and service connections are fully working!")
