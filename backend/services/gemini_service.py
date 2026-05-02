"""
Gemini service module for the ElectIQ backend.
Handles AI generation for chat, quizzes, and facts.
"""
import os
import google.generativeai as genai
from backend.services.db_service import db_service
from backend.utils.constants import GEMINI_MODEL_CHAT, GEMINI_MODEL_QUIZ, GEMINI_MODEL_FACT

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are an expert election education assistant named ElectIQ.
Your goal is to help users understand the election process interactively.
Explain voter registration, polling process, ballot types, electoral college, election timelines, candidate nomination, counting & certification, results & disputes.
Keep your answers engaging, educational, and unbiased.
IMPORTANT: At the end of EVERY response, include a "Did You Know?" election fact relevant to the topic discussed.
Format your response in plain text with markdown for bolding/italics, but do NOT use complex markdown structures that are hard to parse in simple chat UI.
"""

def get_chat_response(email: str, user_message: str) -> str:
    """
    Gets a response from Gemini, maintaining conversation history.
    
    Args:
        email (str): The user's email to fetch chat history.
        user_message (str): The new prompt from the user.
        
    Returns:
        str: AI generated response.
    """
    try:
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL_CHAT,
            system_instruction=SYSTEM_PROMPT
        )
        
        history = db_service.get_chat_history(email)
        chat = model.start_chat(history=history)
        response = chat.send_message(user_message)
        
        db_service.update_chat_history(email, "user", user_message)
        db_service.update_chat_history(email, "model", response.text)
        
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "I'm sorry, I'm having trouble connecting to my knowledge base right now."

def generate_quiz() -> str:
    """
    Generates a 10-question quiz about the election process.
    
    Returns:
        str: JSON formatted array of quiz questions.
    """
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
        model = genai.GenerativeModel(model_name=GEMINI_MODEL_QUIZ)
        response = model.generate_content(prompt)
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

def generate_fact() -> str:
    """
    Generates an interesting Election Fact of the Day.
    
    Returns:
        str: Interesting election fact.
    """
    prompt = "Generate exactly one short, fascinating 'Did you know?' fact about the election process or history. Keep it under 2 sentences. Do not use formatting."
    try:
        model = genai.GenerativeModel(model_name=GEMINI_MODEL_FACT)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating fact: {e}")
        return "Did you know? The first US presidential election was held in 1788."

