"""
Search service module for the ElectIQ backend.
Fetches the latest election-related news and performs Custom Search.
"""
import os
import requests
import logging
from googleapiclient.discovery import build
from backend.config import get_config

config = get_config()

def fetch_election_news() -> list[dict]:
    """
    Fetch top 5 election-related news articles using NewsAPI.org.
    
    Returns:
        list[dict]: A list of dictionaries containing title, snippet, and link.
    """
    api_key = os.getenv("NEWS_API_KEY")
    
    if not api_key:
        logging.warning("Missing NewsAPI.org credentials")
        return []

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "election OR voting OR candidates",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": api_key
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        articles = []
        for item in data.get("articles", []):
            articles.append({
                "title": item.get("title"),
                "snippet": item.get("description"),
                "link": item.get("url")
            })
        return articles
    except Exception as e:
        logging.error(f"Error fetching news: {e}")
        return []

def search_election_topics(query: str) -> list[dict]:
    """
    Search for election topics using Google Custom Search API.
    Falls back to curated static results if credentials are missing or fail.
    
    Args:
        query (str): The search term.
        
    Returns:
        list[dict]: A list of search results with title, link, and snippet.
    """
    api_key = config.GOOGLE_SEARCH_API_KEY
    cx = config.GOOGLE_SEARCH_CX
    
    if api_key and cx:
        try:
            service = build("customsearch", "v1", developerKey=api_key)
            result = service.cse().list(q=query, cx=cx, num=5).execute()
            
            items = []
            for item in result.get('items', []):
                items.append({
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet")
                })
            return items
        except Exception as e:
            logging.error(f"Google Custom Search API error: {e}")
    else:
        logging.warning("Missing Google Search credentials. Falling back to static results.")
        
    # Fallback to curated static results
    return [
        {
            "title": "How to Register to Vote | USAGov",
            "link": "https://www.usa.gov/register-to-vote",
            "snippet": "Learn how to register to vote, check your registration status, and find out what deadlines apply."
        },
        {
            "title": "Electoral College | National Archives",
            "link": "https://www.archives.gov/electoral-college",
            "snippet": "Information about how the Electoral College works, its history, and how votes are cast and counted."
        },
        {
            "title": "Voting and Elections | USA.gov",
            "link": "https://www.usa.gov/voting",
            "snippet": "Find answers to common questions about voting in the United States."
        }
    ]
