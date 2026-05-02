import os
from pymongo import MongoClient
from pymongo.collection import Collection

class DBService:
    def __init__(self):
        self.client = None
        self.db = None
        
        # We only connect if MONGODB_URI is provided
        uri = os.getenv('MONGODB_URI')
        if uri:
            try:
                self.client = MongoClient(uri)
                self.db = self.client['electiq_db']
                # Create indexes for quick lookups
                self.db.users.create_index("email", unique=True)
            except Exception as e:
                print(f"Failed to connect to MongoDB: {e}")

    def get_users_collection(self) -> Collection:
        """Get the users collection, or return None if db not connected."""
        if self.db is not None:
            return self.db.users
        return None

    def get_or_create_user(self, email: str):
        """Find user by email or create a new one."""
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
            # Remove the _id from the returned dict to avoid JSON serialization issues
            user.pop("_id", None)
        else:
            user.pop("_id", None)
            
        return user

    def update_chat_history(self, email: str, role: str, text: str):
        """Append a message to the user's chat history."""
        collection = self.get_users_collection()
        if collection is not None:
            collection.update_one(
                {"email": email},
                {"$push": {"chat_history": {"role": role, "parts": [{"text": text}]}}}
            )

    def get_chat_history(self, email: str):
        """Retrieve user's chat history."""
        user = self.get_or_create_user(email)
        return user.get("chat_history", [])

    def save_quiz_score(self, email: str, score: int, total: int):
        """Save a quiz score for the user."""
        collection = self.get_users_collection()
        if collection is not None:
            collection.update_one(
                {"email": email},
                {"$push": {"quiz_scores": {"score": score, "total": total}}}
            )

# Singleton instance
db_service = DBService()
