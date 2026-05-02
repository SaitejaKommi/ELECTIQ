"""
Firebase Firestore integration module for persistent storage.
Gracefully falls back to MongoDB (via db_service) if credentials are unavailable.
"""
import os
import logging
import firebase_admin
from firebase_admin import credentials, firestore
from backend.services.db_service import db_service
from backend.config import get_config

config = get_config()
_db = None

def init_firebase() -> bool:
    """
    Initializes the Firebase Admin SDK.
    Returns True if successful, False if credentials are missing or invalid.
    """
    global _db
    if _db is not None:
        return True
        
    try:
        # Check for service account key path
        cred_path = config.FIREBASE_CREDENTIALS_PATH
        if cred_path and os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            _db = firestore.client()
            logging.info("Firebase Firestore initialized successfully.")
            return True
        elif os.getenv('FIREBASE_CREDENTIALS_JSON'):
            # Alternative: Load from JSON string in env (for Render)
            import json
            cred_dict = json.loads(os.getenv('FIREBASE_CREDENTIALS_JSON'))
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            _db = firestore.client()
            logging.info("Firebase Firestore initialized successfully from JSON env.")
            return True
        else:
            logging.warning("Firebase credentials not found. Falling back to MongoDB.")
            return False
    except Exception as e:
        logging.error(f"Failed to initialize Firebase: {e}. Falling back to MongoDB.")
        return False

# Attempt to initialize on load
USE_FIREBASE: bool = init_firebase()

def get_or_create_user(email: str) -> dict:
    """
    Retrieve user or create if not exists.
    Uses Firebase if available, else MongoDB.
    """
    if not USE_FIREBASE or _db is None:
        return db_service.get_or_create_user(email)
        
    try:
        user_ref = _db.collection('users').document(email)
        doc = user_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            new_user = {
                "email": email,
                "chat_history": [],
                "quiz_scores": [],
                "glossary_searches": []
            }
            user_ref.set(new_user)
            return new_user
    except Exception as e:
        logging.error(f"Firebase get_or_create_user error: {e}")
        return db_service.get_or_create_user(email)

def update_chat_history(email: str, role: str, text: str) -> None:
    """
    Appends a message to the user's chat history.
    """
    if not USE_FIREBASE or _db is None:
        return db_service.update_chat_history(email, role, text)
        
    try:
        user_ref = _db.collection('users').document(email)
        user_ref.update({
            "chat_history": firestore.ArrayUnion([{"role": role, "text": text}])
        })
    except Exception as e:
        logging.error(f"Firebase update_chat_history error: {e}")
        db_service.update_chat_history(email, role, text)

def save_quiz_score(email: str, score: int, total: int) -> None:
    """
    Appends a quiz score to the user's profile.
    """
    if not USE_FIREBASE or _db is None:
        return db_service.save_quiz_score(email, score, total)
        
    try:
        user_ref = _db.collection('users').document(email)
        user_ref.update({
            "quiz_scores": firestore.ArrayUnion([{"score": score, "total": total}])
        })
    except Exception as e:
        logging.error(f"Firebase save_quiz_score error: {e}")
        db_service.save_quiz_score(email, score, total)

def get_chat_history(email: str) -> list[dict]:
    """
    Retrieves the chat history for context.
    """
    if not USE_FIREBASE or _db is None:
        return db_service.get_chat_history(email)
        
    try:
        doc = _db.collection('users').document(email).get()
        if doc.exists:
            return doc.to_dict().get('chat_history', [])
        return []
    except Exception as e:
        logging.error(f"Firebase get_chat_history error: {e}")
        return db_service.get_chat_history(email)

def save_glossary_search(email: str, term: str) -> None:
    """
    Saves a glossary search term to the user's profile.
    """
    if not USE_FIREBASE or _db is None:
        # Fallback to MongoDB, we must add glossary_searches field
        try:
            db_service.db.users.update_one(
                {"email": email},
                {"$push": {"glossary_searches": term}}
            )
        except Exception:
            pass
        return
        
    try:
        user_ref = _db.collection('users').document(email)
        user_ref.update({
            "glossary_searches": firestore.ArrayUnion([term])
        })
    except Exception as e:
        logging.error(f"Firebase save_glossary_search error: {e}")
