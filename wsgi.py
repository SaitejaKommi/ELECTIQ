import sys
import os

# Add the backend folder to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import the application factory from backend/app.py
from app import create_app

# Create the application instance
app = create_app()

if __name__ == "__main__":
    app.run()
