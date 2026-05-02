"""
Search service module for the ElectIQ backend.
Fetches the latest election-related news.
"""
import os
import requests

def fetch_election_news() -> list:
    """
    Fetch top 5 election-related news articles using NewsAPI.org.
    
    Returns:
        list: A list of dictionaries containing title, snippet, and link.
    """
    api_key = os.getenv("NEWS_API_KEY")
    
    if not api_key:
        print("Missing NewsAPI.org credentials")
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
        print(f"Error fetching news: {e}")
        return []
