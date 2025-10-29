# scraper.py
import requests
from bs4 import BeautifulSoup
import feedparser

def scrape_articles(topic, limit=10):
    """
    Fetch recent articles related to a topic from Google News RSS feed.
    Returns a list of dicts with {title, url, content, summary}.
    """
    query = topic.replace(" ", "+")
    feed_url = f"https://news.google.com/rss/search?q={query}"

    articles = []
    feed = feedparser.parse(feed_url)

    for entry in feed.entries[:limit]:
        title = entry.title
        url = entry.link
        summary = entry.get("summary", "")

        # Try to fetch full text from the article URL
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = [p.get_text() for p in soup.find_all("p")]
            content = " ".join(paragraphs)
        except Exception:
            content = summary or ""

        articles.append({
            "title": title,
            "url": url,
            "summary": summary,
            "content": content
        })

    print(f"✅ Fetched {len(articles)} articles for topic: {topic}")
    return articles
