import feedparser
from datetime import datetime
from app.models import Article

def scrape_huggingface_news():
    print("Scraping HuggingFace news...")
    feed = feedparser.parse("https://huggingface.co/blog/feed.xml")
    articles = []
    for entry in feed.entries:
        article = Article(
            title=entry.title,
            url=entry.link,
            source="HuggingFace",
            published_at=datetime(*entry.published_parsed[:6])
        )
        articles.append(article)
        print(f"Found: {article.title}")
    print(f"Total: {len(articles)} articles")
    return articles