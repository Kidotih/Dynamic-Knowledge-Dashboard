import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def scrape_articles(topic):
    """
    Scrape articles for a given topic.
    Returns a list of dictionaries: [{"title": ..., "content": ...}, ...]
    """

    # Encode topic for URL
    base_url = "https://news.google.com/search?q="
    search_url = f"{base_url}{quote(topic)}"  # safely encode spaces & special chars

    articles = []
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/116.0.0.0 Safari/537.36"
        }
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')

        # Google News articles often have headlines in <h3>
        for item in soup.find_all('article')[:5]:  # limit to first 5 articles
            title_tag = item.find('h3')
            content_tag = item.find('span')  # Google News sometimes uses <span> for summaries
            if title_tag:
                articles.append({
                    "title": title_tag.text.strip(),
                    "content": content_tag.text.strip() if content_tag else ""
                })

    except requests.exceptions.RequestException as e:
        print(f"Error fetching articles: {e}")

    return articles



