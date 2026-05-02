"""
Input sanitizer utility module for the ElectIQ backend.
Provides functions to safely parse and validate user input.
"""
from markupsafe import escape
import re

def sanitize_input(text: str) -> str:
    """
    Sanitize user input by escaping HTML characters
    and stripping leading/trailing whitespace.
    
    Args:
        text (str): Raw user input.
        
    Returns:
        str: Sanitized and safe string.
    """
    if not isinstance(text, str):
        return ""
    # Strip whitespace
    text = text.strip()
    # Escape HTML to prevent XSS
    return str(escape(text))

def is_valid_email(email: str) -> bool:
    """
    Validate basic email format using Regex.
    
    Args:
        email (str): The email string to validate.
        
    Returns:
        bool: True if valid, False otherwise.
    """
    email_regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    return bool(email_regex.match(email))
