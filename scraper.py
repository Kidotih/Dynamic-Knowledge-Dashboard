# scraper.py
import requests
from bs4 import BeautifulSoup

def scrape_articles(topic):
    """
    Scrape articles for a given topic.
    Returns a list of dicts: [{"title": ..., "content": ...}, ...]
    """
    base_url = "https://news.google.com/search?q="
    search_url = f"{base_url}{topic}"

    articles = []
    try:
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for item in soup.find_all("article")[:5]:
            title_tag = item.find("h3")
            content_tag = item.find("p")
            if title_tag:
                articles.append({
                    "title": title_tag.text.strip(),
                    "content": content_tag.text.strip() if content_tag else ""
                })
    except requests.exceptions.RequestException as e:
        print(f"Error fetching articles: {e}")

    return articles
