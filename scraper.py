import requests
from bs4 import BeautifulSoup
import feedparser

def scrape_articles(topic, limit=10, fetch_full_content=False):
    """
    Fetch recent articles related to a topic using Google News RSS.
    
    Args:
        topic (str): The search topic.
        limit (int): Max number of articles to fetch.
        fetch_full_content (bool): If True, fetch full article content from the website.
        
    Returns:
        List of articles with: title, url, summary, content, published, source, image
    """
    
    # Format the topic for URL
    query = topic.replace(" ", "+")
    
    # Google News RSS URL
    feed_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:US"
    
    # Parse the RSS feed
    feed = feedparser.parse(feed_url)
    
    if not feed.entries:
        print(f"⚠ No entries found for topic: {topic}")
        return []

    articles = []

    for entry in feed.entries[:limit]:
        title = entry.title
        url = entry.link
        summary = entry.get("summary", "")
        published = entry.get("published", "")
        # Get source if exists, otherwise parse from URL
        source = getattr(entry, "source", {}).get("title", "") or url.split("/")[2]

        # Fetch full article content if requested
        content = summary
        if fetch_full_content:
            try:
                headers = {"User-Agent": "Mozilla/5.0"}  # Avoid blocking
                response = requests.get(url, headers=headers, timeout=5)
                soup = BeautifulSoup(response.text, "html.parser")
                paragraphs = [p.get_text() for p in soup.find_all("p")]
                if paragraphs:
                    content = " ".join(paragraphs)
            except Exception as e:
                print(f"⚠ Failed to fetch full content for {url}: {e}")
                content = summary

        articles.append({
            "title": title,
            "url": url,
            "summary": summary,
            "content": content,
            "published": published,
            "source": source,
            "image": None
        })

    print(f"✅ Found {len(articles)} articles for topic: {topic}")
    return articles


# Example usage
if __name__ == "__main__":
    topics = ["kenya", "climate", "Manchester united", "premier league"]
    for topic in topics:
        articles = scrape_articles(topic, limit=5, fetch_full_content=False)
        for i, article in enumerate(articles, 1):
            print(f"{i}. {article['title']} ({article['source']})")
            print(f"   URL: {article['url']}")
            print(f"   Summary: {article['summary'][:150]}...\n")
