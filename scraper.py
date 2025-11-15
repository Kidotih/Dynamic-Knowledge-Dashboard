import requests
from bs4 import BeautifulSoup
import feedparser

def scrape_articles(topic, limit=10):
    """
    Fetch recent articles related to a topic using Google News RSS.
    Returns a list of articles with: title, url, summary, content, published, source
    """
    
    query = topic.replace(" ", "+")
    
    # FIXED: latest Google News RSS format
    feed_url = (
        f"https://news.google.com/rss/search?"
        f"tbm=nws&hl=en-US&gl=US&ceid=US:en&q={query}"
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
            headers = {"User-Agent": "Mozilla/5.0"}  # avoids cloud blocking
            response = requests.get(url, headers=headers, timeout=5)
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
            "image": None
        })

    print(f"✅ Found {len(articles)} articles.")
    return articles
