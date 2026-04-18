from sqlalchemy.exc import IntegrityError
from app.models import Article

def save_articles(db, articles):
    saved = 0
    skipped = 0

    for article in articles:
        try:
            db.add(article)
            db.commit()
            saved += 1
        except IntegrityError:
            db.rollback()
            skipped += 1

    print(f"Saved: {saved} new articles | Skipped: {skipped} duplicates")