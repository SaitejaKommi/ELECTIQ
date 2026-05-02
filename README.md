# ElectIQ – Election Process Education Assistant

![Google Gemini API](https://img.shields.io/badge/Google_Gemini-API-blue?logo=google)
![Google Custom Search](https://img.shields.io/badge/Google_Custom_Search-API-blue?logo=google)
![Google Cloud Translate](https://img.shields.io/badge/Google_Cloud_Translate-API-blue?logo=google)
![Google Cloud TTS](https://img.shields.io/badge/Google_Cloud_TTS-API-blue?logo=google)
![Firebase Firestore](https://img.shields.io/badge/Firebase_Firestore-Database-yellow?logo=firebase)
![Google Analytics 4](https://img.shields.io/badge/Google_Analytics_4-Tracking-orange?logo=google-analytics)
![Google Fonts](https://img.shields.io/badge/Google_Fonts-Typography-red?logo=google)
![Coverage](https://img.shields.io/badge/Coverage-86%25-brightgreen.svg)

ElectIQ is a fully interactive, responsive web application that helps users understand the complexities of the election process. Built with a modern Python/Flask backend and a clean Vanilla JS/CSS frontend, ElectIQ uses multiple Google Services to deliver an engaging educational experience.

## Architecture & External Dependencies

```text
                           +--------------------------------------+
                           |             Frontend (SPA)           |
                           | HTML5, CSS3, Vanilla JS              |
                           | Google Fonts (Inter, Roboto Slab)    |
                           | Google Analytics 4 (Event Tracking)  |
                           +------------------+-------------------+
                                              |
                                     REST API | JSON
                                              v
+-----------------------+  +------------------------------------------+  +-----------------------+
|  MongoDB (Fallback)   |--|             Flask Backend                |--|   Firebase Firestore  |
|  (User Data & Chat)   |  |   Rate Limiting, Caching, CORS, Auth     |  |   (User Data & Chat)  |
+-----------------------+  +------------------+-----------------------+  +-----------------------+
                                              |
             +--------------------+-----------+------------+--------------------+
             |                    |                        |                    |
             v                    v                        v                    v
+-------------------------+ +-------------------+ +--------------------+ +--------------------+
|   Google Gemini API     | | Google Custom API | | Google Cloud Trans | | Google Cloud TTS   |
| (Chat, Quiz, Glossary,  | |   (Search Topics) | |  (Translations)    | |  (Text-To-Speech)  |
|  Fact of the Day)       | +-------------------+ +--------------------+ +--------------------+
+-------------------------+
```

## Google Services Integration

ElectIQ deeply integrates 7 real Google Services to provide enterprise-grade capabilities:

1. **Google Gemini API**: 
   - Uses `gemini-2.5-flash` model.
   - **Features**: Interactive Chat Assistant, Quiz Generation, "Fact of the Day", and the Election Glossary.
   - **File**: `backend/services/gemini_service.py`

2. **Google Custom Search API**:
   - Allows users to search the web for election topics directly from the UI.
   - **File**: `backend/services/search_service.py`

3. **Google Cloud Translate API**:
   - Provides on-the-fly translations for all AI responses (Hindi, Spanish, French, Telugu).
   - **File**: `backend/services/translate_service.py`

4. **Google Cloud Text-to-Speech (TTS) API**:
   - Generates natural sounding speech from AI responses for accessibility.
   - **File**: `backend/services/tts_service.py`

5. **Google Firebase Firestore**:
   - Provides secure, persistent storage for user chat history, quiz scores, and glossary queries.
   - **File**: `backend/services/firebase_service.py`

6. **Google Analytics 4**:
   - Deployed directly in the `<head>` of the UI.
   - Triggers custom events for: `quiz_started`, `quiz_completed`, `chat_message_sent`, `glossary_search`, and `language_changed`.
   - **File**: `frontend/index.html` and all `frontend/js/*.js` files.

7. **Google Fonts API**:
   - Powers the typography for the entire UI using *Inter* and *Roboto Slab*.
   - **File**: `frontend/index.html`

## Fallback Strategy
To ensure maximum reliability and graceful degradation, ElectIQ implements strict fallbacks for its services:
- **Firebase Firestore** falls back to **MongoDB** if credentials are missing or initialization fails.
- **Google Cloud Translate** falls back to the **MyMemory API**.
- **Google Cloud TTS** falls back to the browser's native **Web Speech API**.
- **Google Custom Search API** falls back to **curated static results**.
- **NewsAPI** and **Gemini API** are heavily cached (using `Flask-Caching`) to prevent quota exhaustion and rate limit hits.

## Setup & Deployment

1. Set up a virtual environment: `python3 -m venv .venv` and `source .venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure `.env` using `.env.example` as a template.
4. Run locally: `gunicorn -w 1 -b 127.0.0.0:8000 wsgi:app`
5. Test: `python -m pytest --cov=backend tests/`

Designed to be perfectly deployed on Render using the root `wsgi.py` entry point.
