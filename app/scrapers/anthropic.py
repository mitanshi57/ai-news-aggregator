import feedparser
from datetime import datetime
from app.models import Article

def scrape_anthropic_news():
    print("Scraping Anthropic news...")
    feed = feedparser.parse("https://raw.githubusercontent.com/taobojlen/anthropic-rss-feed/main/anthropic_news_rss.xml")
    articles = []
    for entry in feed.entries:
        try:
            article = Article(
                title=entry.title,
                url=entry.link,
                source="Anthropic",
                published_at=datetime(*entry.published_parsed[:6])
            )
            articles.append(article)
            print(f"Found: {article.title}")
        except Exception as e:
            print(f"Skipped one article: {e}")
    print(f"Total: {len(articles)} articles")
    return articles