import feedparser
from datetime import datetime
from app.models import Article

def scrape_mit_tech_review():
    print("Scraping MIT Technology Review...")
    feed = feedparser.parse("https://www.technologyreview.com/topic/artificial-intelligence/feed")
    articles = []
    for entry in feed.entries:
        try:
            article = Article(
                title=entry.title,
                url=entry.link,
                source="MIT Tech Review",
                published_at=datetime(*entry.published_parsed[:6])
            )
            articles.append(article)
            print(f"Found: {article.title}")
        except Exception as e:
            print(f"Skipped: {e}")
    print(f"Total: {len(articles)} articles")
    return articles