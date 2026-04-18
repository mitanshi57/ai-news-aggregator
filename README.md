# AI News Aggregator

This project scrapes AI news sources, stores new articles, summarizes them, and emails a digest of newly summarized articles.

## Gmail digest setup

Add these values to your `.env` file:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_news
GROQ_API_KEY=your_groq_api_key
GMAIL_SENDER_EMAIL=your_gmail_address@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password
DIGEST_RECIPIENT_EMAIL=recipient@gmail.com
```

Notes:

- `GMAIL_APP_PASSWORD` should be a Gmail App Password, not your normal Gmail password.
- If `DIGEST_RECIPIENT_EMAIL` is omitted, the digest is sent to `GMAIL_SENDER_EMAIL`.

## Run

```bash
uv run main.py
```
