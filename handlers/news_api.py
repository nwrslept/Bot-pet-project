import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWSAPI_KEY")
BASE_URL = "https://newsapi.org/v2/top-headlines"

def get_news(category: str, page: int = 1, page_size: int = 5):
    params = {
        "apiKey": API_KEY,
        "category": category,
        "country": "us",
        "page": page,
        "pageSize": page_size
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    print("=== DEBUG RESPONSE ===")
    print(data)

    if data.get("status") != "ok":
        return None, "Помилка при отриманні новин."

    articles = data.get("articles", [])
    if not articles:
        return None, "Новини не знайдено."

    return articles, None
