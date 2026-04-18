import feedparser
from datetime import datetime
from app.models import Article

def scrape_google_research():
    print("Scraping Google Research blog...")
    feed = feedparser.parse("https://research.google/blog/rss")
    articles = []
    for entry in feed.entries:
        try:
            article = Article(
                title=entry.title,
                url=entry.link,
                source="Google Research",
                published_at=datetime(*entry.published_parsed[:6])
            )
            articles.append(article)
            print(f"Found: {article.title}")
        except Exception as e:
            print(f"Skipped: {e}")
    print(f"Total: {len(articles)} articles")
    return articles