from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    url = Column(String(1000), unique=True, nullable=False)
    source = Column(String(100), nullable=False)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    summary = Column(Text, nullable=True)