import requests
from bs4 import BeautifulSoup
from datetime import datetime
from app.models import Article

def scrape_mistral_news():
    print("Scraping Mistral news...")
    
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get("https://mistral.ai/news", headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    articles = []
    
    # Find all news article links
    links = soup.find_all("a", href=True)
    seen_urls = set()
    
    for link in links:
        href = link["href"]
        # Only get news article links
        if href.startswith("/news/") and href != "/news/" and href not in seen_urls:
            seen_urls.add(href)
            full_url = f"https://mistral.ai{href}"
            title = link.get_text(strip=True)
            if title:
                article = Article(
                    title=title,
                    url=full_url,
                    source="Mistral",
                    published_at=datetime.utcnow()
                )
                articles.append(article)
                print(f"Found: {title}")
    
    print(f"Total: {len(articles)} articles")
    return articles