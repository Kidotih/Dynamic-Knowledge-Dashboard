import requests
from bs4 import BeautifulSoup, FeatureNotFound

def scrape_articles(topic):
    """
    Fetch latest news articles from Google News RSS for a given topic.
    Returns a list of dicts: [{"title": ..., "content": ..., "url": ...}, ...]
    """
    rss_url = f"https://news.google.com/rss/search?q={topic}"
    articles = []

    try:
        response = requests.get(rss_url, timeout=10)
        response.raise_for_status()

        # Try XML parser first, fallback to html.parser if not available
        try:
            soup = BeautifulSoup(response.content, "xml")
        except FeatureNotFound:
            soup = BeautifulSoup(response.content, "html.parser")

        items = soup.find_all("item")

        for item in items[:5]:  # Limit to top 5
            title = item.title.text if item.title else "No title"
            description = item.description.text if item.description else "No description"
            link = item.link.text if item.link else ""

            articles.append({
                "title": title,
                "summary": description,
                "url": link
            })

        if not articles:
            print(f"⚠️ No articles found for {topic}.")
        else:
            print(f"✅ Found {len(articles)} articles for '{topic}'")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching articles: {e}")

    return articles
