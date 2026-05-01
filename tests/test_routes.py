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

@patch('routes.chat.get_chat_response')
def test_chat_success(mock_gemini, client):
    mock_gemini.return_value = "This is a mock response"
    response = client.post('/api/chat/', json={"email": "test@example.com", "message": "hello"})
    assert response.status_code == 200
    assert json.loads(response.data)["response"] == "This is a mock response"

def test_chat_empty_input(client):
    response = client.post('/api/chat/', json={"email": "test@example.com", "message": ""})
    assert response.status_code == 400

@patch('routes.quiz.generate_quiz')
def test_quiz_success(mock_quiz, client):
    mock_quiz.return_value = '[{"question": "test", "options": ["A", "B"], "correct_index": 0, "explanation": "test"}]'
    response = client.get('/api/quiz/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]["question"] == "test"

@patch('routes.news.fetch_election_news')
def test_news_success(mock_news, client):
    mock_news.return_value = [{"title": "News 1", "snippet": "Snippet 1", "link": "http://link.com"}]
    response = client.get('/api/news/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1

@patch('routes.translate.translate_text')
def test_translate_success(mock_trans, client):
    mock_trans.return_value = "Hola"
    response = client.post('/api/translate/', json={"text": "Hello", "target_language": "es"})
    assert response.status_code == 200
    assert json.loads(response.data)["translatedText"] == "Hola"
