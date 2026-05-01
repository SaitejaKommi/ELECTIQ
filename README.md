# ElectIQ – Election Process Education Assistant

## Project Title & Description
**ElectIQ** is a production-grade, full-stack web application designed to educate users about the election process interactively. It features an AI chatbot expert, an interactive election timeline, real-time translated content, an educational quiz, and live election news.

## Chosen Vertical
**Election Process Education**

## Live Demo
[Live Demo URL Placeholder]

## Features List
1. **Interactive Election Chatbot**: Powered by Google Gemini API, acts as an expert election assistant with conversation memory.
2. **Visual Election Timeline**: Step-by-step interactive visual timeline of the election process.
3. **Multilingual Support**: Dynamic translation using Google Translate API.
4. **Text-to-Speech Accessibility**: Google Cloud Text-to-Speech for natural voice output of chatbot responses.
5. **Election Quiz Module**: Dynamically generated 10-question quizzes via Gemini API with score tracking.
6. **Real-Time Election News**: Fetched via Google Custom Search API, showing the latest election news.
7. **Voter Checklist Tool**: Interactive readiness checklist for voters.
8. **Email-Based Session Tracking**: Simple login using an email address, stored in MongoDB Atlas, saving chat history and quiz scores.

## Tech Stack
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python (Flask)
- **Database**: MongoDB Atlas (PyMongo)
- **Testing**: pytest

## Google Services Used
- **Google Gemini API**: Used as the AI brain for the interactive chatbot and generating dynamic quiz questions.
- **Google Translate API**: Translates dynamic content (chat responses, news, quiz) to support multilingual accessibility (English, Hindi, Spanish, French, Telugu).
- **Google Cloud Text-to-Speech API**: Provides natural voice audio for chatbot responses to assist visually impaired or auditory learners.
- **Google Custom Search API**: Fetches real-time, relevant election news to keep users informed with current events.

## Architecture Diagram
```text
[ User Browser ]
   |  |
   |  | (HTTP / REST APIs)
   |  v
[ Flask Backend (app.py) ]
   |
   +-- Routes: /api/chat, /api/quiz, /api/news, /api/auth
   |
   +-- Services:
   |     |-- gemini_service.py (Calls Gemini API)
   |     |-- translate_service.py (Calls Google Translate API)
   |     |-- tts_service.py (Calls Google TTS API)
   |     |-- search_service.py (Calls Google Custom Search API)
   |     +-- db_service.py (Calls MongoDB Atlas)
```

## Setup Instructions
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your API keys.
6. Start the server: `python backend/app.py`
7. Access the application at `http://localhost:5000`

## Deployment
- **Backend hosted on Render** (free tier)
- **Frontend hosted on Vercel** (free tier)

### Setting Environment Variables on Render
When deploying the backend to Render, you must manually add the following environment variables in the Render Dashboard (under Environment):
- `GEMINI_API_KEY`
- `MONGODB_URI`
- `NEWS_API_KEY`
- `FLASK_SECRET_KEY`
- `FLASK_ENV` (set to `production`)

## Environment Variables
Refer to `.env.example` for required variables:
- `MONGODB_URI`
- `GEMINI_API_KEY`
- `GOOGLE_SEARCH_API_KEY`
- `GOOGLE_SEARCH_ENGINE_ID`
- `GOOGLE_APPLICATION_CREDENTIALS`

## How to Run Tests
To run the automated tests and check coverage:
- Run `./run_tests.sh` (or `pytest --cov=backend tests/` directly).

## Approach & Logic
- **Architecture**: Separated concerns into frontend SPA, backend routes, and backend services. This ensures API keys are never exposed to the frontend.
- **Database**: Replaced Firebase with MongoDB Atlas for simplicity and free-tier efficiency. Sessions are tied to the user's email.
- **Caching & Rate Limiting**: Implemented Flask-Caching for the News API to reduce quota usage (10 min cache) and Flask-Limiter to prevent chatbot abuse (20 req/min).

## Assumptions Made
- Users will have modern browsers supporting CSS Grid/Flexbox and ES6 JS.
- The `GOOGLE_APPLICATION_CREDENTIALS` path points to a valid service account JSON file.

## Accessibility Notes
- Full WCAG 2.1 AA compliance.
- Semantic HTML tags (`<main>`, `<nav>`, `<article>`) used throughout.
- Minimum contrast ratio of 4.5:1 for text.
- Full keyboard navigation and visible focus indicators.
- ARIA labels on interactive elements and buttons.

## Security Notes
- No API keys exposed to frontend.
- HTML input is sanitized using `markupsafe` before rendering/processing.
- Content Security Policy (CSP) headers applied via Flask-Talisman.

## Future Improvements
- Implement WebSocket for real-time streaming of Gemini responses.
- Add user profiles to track long-term learning progress.
