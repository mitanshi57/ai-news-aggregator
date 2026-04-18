@echo off
cd C:\Users\91635\Documents\ai-news-aggregator
docker start ai_news_db
timeout /t 5
call .venv\Scripts\activate.bat
python main.py