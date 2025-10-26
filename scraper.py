import requests
from bs4 import BeautifulSoup

def scrape_articles(url="https://www.example.com/news"):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []
    
    for item in soup.find_all('article')[:5]:  # Limit to first 5 articles
        title = item.find('h2').text
        content = item.find('p').text
        articles.append({"title": title, "content": content})
    
    return articles
