import json
from unittest.mock import patch
import pytest

def test_login_success(client):
    response = client.post('/api/auth/login', json={"email": "test@example.com"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["email"] == "test@example.com"

def test_login_invalid_email(client):
    response = client.post('/api/auth/login', json={"email": "not-an-email"})
    assert response.status_code == 400

@patch('backend.routes.chat.get_chat_response')
def test_chat_success(mock_gemini, client):
    mock_gemini.return_value = "This is a mock response"
    response = client.post('/api/chat/', json={"email": "test@example.com", "message": "hello"})
    assert response.status_code == 200
    assert json.loads(response.data)["response"] == "This is a mock response"

def test_chat_empty_input(client):
    response = client.post('/api/chat/', json={"email": "test@example.com", "message": ""})
    assert response.status_code == 400

@patch('backend.routes.quiz.generate_quiz')
def test_quiz_get_success(mock_quiz, client):
    mock_quiz.return_value = '[{"question": "test", "options": ["A", "B"], "correct_index": 0, "explanation": "test"}]'
    response = client.get('/api/quiz/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]["question"] == "test"

@patch('backend.routes.quiz.save_quiz_score')
def test_quiz_score_success(mock_save, client):
    response = client.post('/api/quiz/score', json={"email": "test@example.com", "score": 8, "total": 10})
    assert response.status_code == 200


@patch('backend.routes.news.fetch_election_news')
def test_news_success(mock_news, client):
    mock_news.return_value = [{"title": "News 1", "snippet": "Snippet 1", "link": "http://link.com"}]
    response = client.get('/api/news/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1

@patch('backend.routes.translate.translate_text')
def test_translate_success(mock_trans, client):
    mock_trans.return_value = "Hola"
    response = client.post('/api/translate/', json={"text": "Hello", "target_language": "es"})
    assert response.status_code == 200
    assert json.loads(response.data)["translatedText"] == "Hola"

@patch('backend.routes.fact.generate_fact')
def test_fact_success(mock_fact, client):
    mock_fact.return_value = "This is a test fact."
    response = client.get('/api/fact/')
    assert response.status_code == 200
    assert json.loads(response.data)["fact"] == "This is a test fact."

def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert b"healthy" in response.data

@patch('backend.routes.glossary.generate_glossary_term')
def test_glossary_endpoint_success(mock_generate, client):
    mock_generate.return_value = "This is a test term."
    response = client.post('/api/glossary/', json={"term": "Electoral College"})
    assert response.status_code == 200
    assert response.json["term"] == "Electoral College"
    assert response.json["explanation"] == "This is a test term."

def test_glossary_endpoint_missing_term(client):
    response = client.post('/api/glossary/', json={})
    assert response.status_code == 400

@patch('backend.routes.search.search_election_topics')
def test_search_endpoint_success(mock_search, client):
    mock_search.return_value = [{"title": "Test Title", "link": "http://test", "snippet": "Test snippet"}]
    response = client.get('/api/search/?q=voting')
    assert response.status_code == 200
    assert response.json["results"][0]["title"] == "Test Title"

def test_search_endpoint_missing_query(client):
    response = client.get('/api/search/')
    assert response.status_code == 400

@patch('backend.routes.tts.generate_speech')
def test_tts_endpoint_success(mock_speech, client):
    mock_speech.return_value = "YXVkaW8="
    response = client.post('/api/tts/', json={"text": "hello", "language_code": "en-US"})
    assert response.status_code == 200
    assert response.json["audioContent"] == "YXVkaW8="

def test_tts_endpoint_missing_text(client):
    response = client.post('/api/tts/', json={})
    assert response.status_code == 400
