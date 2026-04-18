import feedparser
from datetime import datetime
from app.models import Article

def scrape_openai_news():
    print("Scraping OpenAI news...")
    
    feed_url = "https://openai.com/news/rss.xml"
    feed = feedparser.parse(feed_url)
    
    articles = []
    
    for entry in feed.entries:
        article = Article(
            title=entry.title,
            url=entry.link,
            source="OpenAI",
            published_at=datetime(*entry.published_parsed[:6])
        )
        articles.append(article)
        print(f"Found: {article.title}")
    
    print(f"\nTotal articles found: {len(articles)}")
    return articles