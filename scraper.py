import requests
from bs4 import BeautifulSoup

def scrape_articles(topic, limit=10):
    """
    Fetches recent news articles related to a topic.
    Returns a list of dicts: [{title, url, content}]
    """
    articles = []
    query = topic.replace(" ", "+")
    url = f"https://news.google.com/search?q={query}&hl=en&gl=US&ceid=US:en"

    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        print(f"⚠️ Failed to fetch articles for {topic}")
        return []

    soup = BeautifulSoup(res.text, "html.parser")
    news_cards = soup.select("article")

    for card in news_cards[:limit]:
        title_el = card.select_one("h3")
        if not title_el:
            continue

        title = title_el.get_text()
        link_tag = title_el.find("a")
        url = f"https://news.google.com{link_tag['href'][1:]}" if link_tag else "#"

        # Fetch article content preview
        snippet = ""
        para = card.find("span")
        if para:
            snippet = para.get_text()

        articles.append({
            "title": title,
            "url": url,
            "content": snippet
        })

    print(f"✅ Scraped {len(articles)} articles for topic: {topic}")
    return articles
