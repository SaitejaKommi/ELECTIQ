"""
Cache utility module for the ElectIQ backend.
Initializes the Flask-Caching instance.
"""
from flask_caching import Cache

# Initialize simple in-memory cache
cache = Cache()
