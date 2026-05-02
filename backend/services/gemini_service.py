import os
import google.generativeai as genai
from services.db_service import db_service

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use a standard model
MODEL_NAME = "gemini-2.5-flash"

SYSTEM_PROMPT = """You are an expert election education assistant named ElectIQ.
Your goal is to help users understand the election process interactively.
Explain voter registration, polling process, ballot types, electoral college, election timelines, candidate nomination, counting & certification, results & disputes.
Keep your answers engaging, educational, and unbiased.
IMPORTANT: At the end of EVERY response, include a "Did You Know?" election fact relevant to the topic discussed.
Format your response in plain text with markdown for bolding/italics, but do NOT use complex markdown structures that are hard to parse in simple chat UI.
"""

def get_chat_response(email: str, user_message: str) -> str:
    """Gets a response from Gemini, maintaining conversation history."""
    try:
        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            system_instruction=SYSTEM_PROMPT
        )
        
        # Retrieve history from DB
        history = db_service.get_chat_history(email)
        
        # Start a chat session with the model, providing history
        chat = model.start_chat(history=history)
        
        # Send the message
        response = chat.send_message(user_message)
        
        # Save both user and model message to DB
        db_service.update_chat_history(email, "user", user_message)
        db_service.update_chat_history(email, "model", response.text)
        
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "I'm sorry, I'm having trouble connecting to my knowledge base right now."

def generate_quiz() -> str:
    """Generates a 10-question quiz about the election process."""
    prompt = """Generate a 10-question interactive quiz about general election processes (registration, voting, counting, etc.).
    Respond ONLY with a raw JSON array of objects. Do not include markdown formatting like ```json or anything else.
    Format exactly like this:
    [
      {
        "question": "What is the primary purpose of a primary election?",
        "options": ["To elect the President", "To choose party candidates", "To pass laws", "To recall a politician"],
        "correct_index": 1,
        "explanation": "Primary elections are used by political parties to select their nominees for the general election."
      }
    ]
    """
    try:
        model = genai.GenerativeModel(model_name=MODEL_NAME)
        response = model.generate_content(prompt)
        # Strip potential markdown blocks
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
    except Exception as e:
        print(f"Error generating quiz: {e}")
        return "[]"
