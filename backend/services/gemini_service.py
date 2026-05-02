"""
Gemini service module for the ElectIQ backend.
Handles AI generation for chat, quizzes, facts, and glossary terms.
"""
import os
import google.generativeai as genai
from backend.services.firebase_service import get_chat_history, update_chat_history
from backend.utils.constants import GEMINI_MODEL_CHAT, GEMINI_MODEL_QUIZ, GEMINI_MODEL_FACT, GEMINI_MODEL_GLOSSARY

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
        
        history = get_chat_history(email)
        chat = model.start_chat(history=history)
        response = chat.send_message(user_message)
        
        update_chat_history(email, "user", user_message)
        update_chat_history(email, "model", response.text)
        
        return response.text
    except Exception as e:
        import logging
        logging.error(f"Error calling Gemini API: {e}")
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
        import logging
        logging.error(f"Error generating quiz: {e}")
        return "[]"

def generate_fact() -> str:
    """
    Generates a single, interesting election fact using Gemini.
    
    Returns:
        str: The generated fact or a fallback fact.
    """
    try:
        model = genai.GenerativeModel(GEMINI_MODEL_FACT)
        prompt = "Provide a single, short, fascinating, and educational 'Did you know?' fact about the election process or election history. Do not use formatting. Just the text."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        import logging
        logging.error(f"Error generating fact: {e}")
        return "Did you know? The first US presidential election was held in 1788."

def generate_glossary_term(term: str) -> str:
    """
    Generates a simple explanation for an election term using Gemini.
    
    Args:
        term (str): The term to explain.
        
    Returns:
        str: The explanation.
    """
    try:
        model = genai.GenerativeModel(GEMINI_MODEL_GLOSSARY)
        prompt = f"Explain the election term '{term}' in simple, easy-to-understand language. Keep it under 3 sentences. If the term is not related to elections, voting, or politics, politely decline to explain it."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        import logging
        logging.error(f"Error generating glossary term: {e}")
        return "Unable to retrieve explanation at this time. Please try again later."
