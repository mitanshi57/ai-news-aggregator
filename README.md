# 🤖 AI News Aggregator

A tool that automatically collects the latest AI news from 7 top sources, summarizes each article using AI, and delivers a clean digest straight to your email inbox every day.

---

## What It Does

Every time you run this project, it:

1. **Scrapes** the latest articles from 7 AI news sources
2. **Saves** them to a database (skipping ones already saved)
3. **Summarizes** new articles using AI (Groq's free Llama model)
4. **Emails** you a formatted digest with titles, sources, and summaries

---

## News Sources

| Source                | Type |
|-----------------------|------|
| OpenAI                | Official blog (RSS) 
| Anthropic             | Official blog (RSS) 
| Google DeepMind       | Official blog (RSS) 
| Hugging Face          | Official blog (RSS) 
| Google Research       | Official blog (RSS) 
| MIT Technology Review | AI section (RSS)     
| Mistral AI            | Official news page (Web scraping) 

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Main programming language |
| PostgreSQL | Database to store articles |
| Docker | Runs the database locally |
| SQLAlchemy | Python library to talk to the database |
| feedparser | Parses RSS feeds |
| BeautifulSoup | Scrapes websites directly |
| Groq API (free) | AI summarization using Llama 3 |
| smtplib | Sends emails via Gmail |
| python-dotenv | Manages secret keys safely |

---

## How to Run It Yourself

### 1. Clone the repository
```bash
git clone https://github.com/mitanshi57/ai-news-aggregator.git
cd ai-news-aggregator
```

### 2. Install dependencies
```bash
uv install
```

### 3. Set up your environment variables
Create a `.env` file in the root folder:
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_news
GROQ_API_KEY=your_groq_api_key_here
EMAIL_SENDER=your_gmail@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_RECEIVER=your_gmail@gmail.com

### 4. Start the database
```bash
cd docker
docker compose up -d
cd ..
```

### 5. Run the aggregator
```bash
python main.py
```

That's it! Check your inbox for the AI news digest 📧

---

## Getting Your API Keys

### Groq API Key (Free)
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up with Google
3. Go to API Keys → Create new key
4. Paste it in your `.env` file

### Gmail App Password
1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Security → Enable 2-Step Verification
3. Search "App passwords" → Create one
4. Paste the 16-character password in your `.env` file

---

## Project Structure
ai-news-aggregator/
├── app/
│   ├── scrapers/
│   │   ├── openai.py
│   │   ├── anthropic.py
│   │   ├── deepmind.py
│   │   ├── huggingface.py
│   │   ├── mistral.py
│   │   ├── mit_tech_review.py
│   │   └── google_research.py
│   ├── services/
│   │   ├── database.py
│   │   ├── article_service.py
│   │   ├── summarizer.py
│   │   └── email_service.py
│   └── models.py
├── docker/
│   └── docker-compose.yml
├── main.py
├── .env
└── pyproject.toml

## Built By
Mitanshi P. Asnani
Building real projects to learn AI & Data Science 
