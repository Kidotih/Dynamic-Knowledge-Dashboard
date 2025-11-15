import requests
from bs4 import BeautifulSoup
import feedparser

def scrape_articles(topic, limit=10):
    """
    Fetch recent articles related to a topic using Google News RSS.
    Returns a list of articles with: title, url, summary, content, published, source
    """
    
    query = topic.replace(" ", "+")
    
    # Updated RSS format (Google changed this recently)
    feed_url = (
        f"https://news.google.com/rss/search?q={query}"
        "&hl=en-US&gl=US&ceid=US:en"
    )

    articles = []
    feed = feedparser.parse(feed_url)

    if not feed.entries:
        print("⚠ No entries returned from Google. Topic:", topic)
        return []

    for entry in feed.entries[:limit]:
        title = entry.title
        url = entry.link
        summary = entry.get("summary", "")
        published = entry.get("published", "")
        source = entry.get("source", {}).get("title", "")

        # Fetch full article content
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = [p.get_text() for p in soup.find_all("p")]
            content = " ".join(paragraphs)
        except:
            content = summary or ""

        articles.append({
            "title": title,
            "url": url,
            "summary": summary,
            "content": content,
            "published": published,
            "source": source,
            "image": None  # reserved for the next upgrade
        })

    print(f"✅ Found {len(articles)} articles.")
    return articles
