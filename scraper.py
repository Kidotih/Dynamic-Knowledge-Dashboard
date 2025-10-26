import requests
from bs4 import BeautifulSoup

def scrape_articles(url="https://www.example.com/news"):
    articles = []
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for item in soup.find_all('article')[:5]:  # Limit to first 5 articles
            title_tag = item.find('h2')
            content_tag = item.find('p')
            if title_tag and content_tag:
                articles.append({
                    "title": title_tag.text.strip(),
                    "content": content_tag.text.strip()
                })
    except requests.exceptions.RequestException as e:
        print(f"Error fetching articles: {e}")
    
    return articles

