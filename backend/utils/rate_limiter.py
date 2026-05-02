"""
Rate limiter utility module for the ElectIQ backend.
Initializes the Flask-Limiter instance.
"""
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from backend.utils.constants import DEFAULT_RATE_LIMIT

# Initialize rate limiter using client IP
# In a real production setup, consider using Redis for the storage backend
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[DEFAULT_RATE_LIMIT],
    storage_uri="memory://"
)
