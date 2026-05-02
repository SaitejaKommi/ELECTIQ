from unittest.mock import patch, MagicMock
from backend.services.search_service import fetch_election_news
from backend.services.translate_service import translate_text
from backend.services.gemini_service import get_chat_response, generate_quiz, generate_fact
from backend.services.db_service import db_service

@patch('backend.services.search_service.requests.get')
def test_fetch_election_news_success(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"articles": [{"title": "T1", "description": "D1", "url": "U1"}]}
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response
    
    with patch('backend.services.search_service.os.getenv', return_value='fake_key'):
        articles = fetch_election_news()
        assert len(articles) == 1
        assert articles[0]["title"] == "T1"

@patch('backend.services.search_service.requests.get')
def test_fetch_election_news_failure(mock_get):
    mock_get.side_effect = Exception("Network Error")
    with patch('backend.services.search_service.os.getenv', return_value='fake_key'):
        articles = fetch_election_news()
        assert len(articles) == 0

def test_fetch_election_news_no_key():
    with patch('backend.services.search_service.os.getenv', return_value=None):
        articles = fetch_election_news()
        assert len(articles) == 0

@patch('backend.services.translate_service.requests.get')
def test_translate_text_success(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"responseData": {"translatedText": "Hola"}}
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response
    
    text = translate_text("Hello", "es")
    assert text == "Hola"

@patch('backend.services.translate_service.requests.get')
def test_translate_text_failure(mock_get):
    mock_get.side_effect = Exception("Error")
    text = translate_text("Hello", "es")
    assert text == "Hello"

def test_translate_text_en():
    assert translate_text("Hello", "en") == "Hello"

@patch('backend.services.gemini_service.genai.GenerativeModel')
def test_get_chat_response(mock_model):
    mock_instance = MagicMock()
    mock_chat = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Mock AI Response"
    mock_chat.send_message.return_value = mock_response
    mock_instance.start_chat.return_value = mock_chat
    mock_model.return_value = mock_instance
    
    with patch('backend.services.gemini_service.db_service') as mock_db:
        mock_db.get_chat_history.return_value = []
        response = get_chat_response("test@example.com", "hello")
        assert response == "Mock AI Response"

@patch('backend.services.gemini_service.genai.GenerativeModel')
def test_generate_quiz(mock_model):
    mock_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "```json\n[]\n```"
    mock_instance.generate_content.return_value = mock_response
    mock_model.return_value = mock_instance
    
    quiz = generate_quiz()
    assert quiz == "[]"

@patch('backend.services.gemini_service.genai.GenerativeModel')
def test_generate_fact(mock_model):
    mock_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Fact!"
    mock_instance.generate_content.return_value = mock_response
    mock_model.return_value = mock_instance
    
    fact = generate_fact()
    assert fact == "Fact!"

def test_db_service_fallback():
    # Test DB fallback when MONGODB_URI is None
    user = db_service.get_or_create_user("test@example.com")
    assert user["email"] == "test@example.com"
    assert db_service.get_chat_history("test@example.com") == []
    
    # These should not crash
    db_service.update_chat_history("test@example.com", "user", "text")
    db_service.save_quiz_score("test@example.com", 10, 10)

def test_db_service_with_mock_db(monkeypatch):
    from mongomock import MongoClient
    client = MongoClient()
    db_service.client = client
    db_service.db = client.test_db
    
    # Reset mock from conftest
    monkeypatch.undo()
    
    # Test insert
    user = db_service.get_or_create_user("real@example.com")
    assert user["email"] == "real@example.com"
    assert "_id" not in user
    
    # Test update and get history
    db_service.update_chat_history("real@example.com", "user", "hi")
    history = db_service.get_chat_history("real@example.com")
    assert len(history) == 1
    assert history[0]["role"] == "user"
    
    # Test save score
    db_service.save_quiz_score("real@example.com", 8, 10)
    user2 = db_service.get_or_create_user("real@example.com")
    assert len(user2["quiz_scores"]) == 1
    assert user2["quiz_scores"][0]["score"] == 8

@patch('backend.services.gemini_service.genai.GenerativeModel')
def test_gemini_exceptions(mock_model):
    mock_instance = MagicMock()
    mock_instance.generate_content.side_effect = Exception("API Down")
    mock_model.return_value = mock_instance
    
    assert generate_quiz() == "[]"
    assert generate_fact() == "Did you know? The first US presidential election was held in 1788."
