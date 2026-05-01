import pytest
from backend.app import create_app
from backend.services.db_service import db_service

@pytest.fixture
def app():
    app = create_app({"TESTING": True, "CACHE_TYPE": "SimpleCache"})
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def mock_db(monkeypatch):
    """Mock the DB service to return simple dicts without Mongo calls"""
    def mock_get_user(email):
        return {"email": email, "chat_history": [], "quiz_scores": []}
    def mock_update(email, role, text):
        pass
    def mock_save(email, score, total):
        pass
    def mock_history(email):
        return []
        
    monkeypatch.setattr(db_service, "get_or_create_user", mock_get_user)
    monkeypatch.setattr(db_service, "update_chat_history", mock_update)
    monkeypatch.setattr(db_service, "save_quiz_score", mock_save)
    monkeypatch.setattr(db_service, "get_chat_history", mock_history)
