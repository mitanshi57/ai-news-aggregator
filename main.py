from app.services.database import init_db, get_db
from app.services.article_service import save_articles
from app.services.summarizer import summarize_article
from app.services.email_service import send_digest_email
from app.scrapers.openai import scrape_openai_news
from app.scrapers.anthropic import scrape_anthropic_news
from app.scrapers.deepmind import scrape_deepmind_news
from app.scrapers.huggingface import scrape_huggingface_news
from app.scrapers.mistral import scrape_mistral_news
from app.scrapers.mit_tech_review import scrape_mit_tech_review
from app.scrapers.google_research import scrape_google_research
from app.models import Article

def main():
    print("Starting AI News Aggregator...\n")

    # Step 1: Make sure database tables exist
    init_db()

    # Step 2: Get a database session
    db = next(get_db())

    # Step 3: Scrape from ALL sources
    all_articles = []
    all_articles += scrape_openai_news()
    all_articles += scrape_anthropic_news()
    all_articles += scrape_deepmind_news()
    all_articles += scrape_huggingface_news()
    all_articles += scrape_mistral_news()
    all_articles += scrape_mit_tech_review()
    all_articles += scrape_google_research()

    print(f"\nTotal articles scraped: {len(all_articles)}")

    # Step 4: Save to database
    save_articles(db, all_articles)

    # Step 5: Summarize unsummarized articles
    print("\nSummarizing new articles...")
    unsummarized = db.query(Article).filter_by(summary=None).all()
    print(f"Found {len(unsummarized)} articles to summarize")

    newly_summarized = []
    for article in unsummarized[:5]:
        print(f"\nSummarizing: {article.title}")
        article.summary = summarize_article(article.title, article.url)
        db.commit()
        newly_summarized.append(article)
        print(article.summary)

    # Step 6: Send email digest
    print("\nSending email digest...")
    send_digest_email(newly_summarized)

    print("\nDone!")

if __name__ == "__main__":
    main()