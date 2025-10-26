import requests
from bs4 import BeautifulSoup

def scrape_articles(topic):
    """
    Scrape articles for a given topic.
    Returns a list of dictionaries: [{"title": ..., "content": ...}, ...]
    """

    # Example using Google News search
    base_url = "https://news.google.com/search?q="
    search_url = f"{base_url}{topic}"

    articles = []
    try:
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for item in soup.find_all('article')[:5]:  # Limit to first 5 articles
            title_tag = item.find('h3')  # Google News headlines are in <h3>
            content_tag = item.find('p')  # Some sites may have <p> summaries
            if title_tag:
                articles.append({
                    "title": title_tag.text.strip(),
                    "content": content_tag.text.strip() if content_tag else ""
                })
    except requests.exceptions.RequestException as e:
        print(f"Error fetching articles: {e}")
    
    return articles


