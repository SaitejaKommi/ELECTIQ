"""
Database service module for the ElectIQ backend.
Handles MongoDB connections, pooling, and user data retrieval.
"""
import os
from pymongo import MongoClient
from pymongo.collection import Collection

class DBService:
    """
    Service class managing MongoDB connections and operations.
    Implements connection pooling natively via PyMongo's MongoClient.
    """
    def __init__(self):
        """Initializes MongoDB connection and creates required indexes."""
        self.client = None
        self.db = None
        
        # PyMongo naturally handles connection pooling under the hood
        # maxPoolSize defaults to 100 which is highly efficient.
        uri = os.getenv('MONGODB_URI')
        if uri:
            try:
                self.client = MongoClient(uri)
                self.db = self.client['electiq_db']
                # Create indexes for quick lookups on email
                self.db.users.create_index("email", unique=True)
            except Exception as e:
                print(f"Failed to connect to MongoDB: {e}")

    def get_users_collection(self) -> Collection:
        """
        Get the users collection.
        
        Returns:
            Collection: PyMongo collection object or None.
        """
        if self.db is not None:
            return self.db.users
        return None

    def get_or_create_user(self, email: str) -> dict:
        """
        Find user by email or create a new one.
        
        Args:
            email (str): User's email address.
            
        Returns:
            dict: User data dictionary.
        """
        collection = self.get_users_collection()
        if collection is None:
            # Fallback for testing/no-db mode
            return {"email": email, "chat_history": [], "quiz_scores": []}
            
        user = collection.find_one({"email": email})
        if not user:
            user = {
                "email": email,
                "chat_history": [],
                "quiz_scores": []
            }
            collection.insert_one(user)
            user.pop("_id", None)
        else:
            user.pop("_id", None)
            
        return user

    def update_chat_history(self, email: str, role: str, text: str):
        """
        Append a message to the user's chat history.
        
        Args:
            email (str): User's email address.
            role (str): 'user' or 'model'.
            text (str): Chat text content.
        """
        collection = self.get_users_collection()
        if collection is not None:
            collection.update_one(
                {"email": email},
                {"$push": {"chat_history": {"role": role, "parts": [{"text": text}]}}}
            )

    def get_chat_history(self, email: str) -> list:
        """
        Retrieve user's chat history.
        
        Args:
            email (str): User's email address.
            
        Returns:
            list: List of chat history objects.
        """
        user = self.get_or_create_user(email)
        return user.get("chat_history", [])

    def save_quiz_score(self, email: str, score: int, total: int):
        """
        Save a quiz score for the user.
        
        Args:
            email (str): User's email address.
            score (int): Score achieved.
            total (int): Total possible score.
        """
        collection = self.get_users_collection()
        if collection is not None:
            collection.update_one(
                {"email": email},
                {"$push": {"quiz_scores": {"score": score, "total": total}}}
            )

# Singleton instance
db_service = DBService()
