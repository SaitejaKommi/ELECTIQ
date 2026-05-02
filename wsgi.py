# Import the application factory directly from the backend package
from backend.app import create_app

# Create the application instance
app = create_app()

if __name__ == "__main__":
    app.run()
