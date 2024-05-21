from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URI = 'sqlite:////Users/borislavvoytash/Desktop/repos/etl_app/news_scraper/news_scraper/news.db'  # Use your SQLite database URI

Base = declarative_base()


class NewsArticle(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    url = Column(String, unique=True, index=True)
    author = Column(String, index=True)
    publication_date = Column(DateTime)
    image_urls = Column(Text)  # Comma-separated URLs
    body = Column(Text)
    ner_entities = Column(Text)  # JSON serialized entities


# Create engine and session
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)