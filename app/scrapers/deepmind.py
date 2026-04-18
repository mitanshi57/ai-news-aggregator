import feedparser
from datetime import datetime
from app.models import Article

def scrape_deepmind_news():
    print("Scraping DeepMind news...")
    feed = feedparser.parse("https://deepmind.google/blog/rss.xml")
    articles = []
    for entry in feed.entries:
        article = Article(
            title=entry.title,
            url=entry.link,
            source="DeepMind",
            published_at=datetime(*entry.published_parsed[:6])
        )
        articles.append(article)
        print(f"Found: {article.title}")
    print(f"Total: {len(articles)} articles")
    return articles