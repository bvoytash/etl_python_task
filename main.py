from fastapi.params import Query
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, desc, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session, session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from typing import List, Optional
import uvicorn
import json
import logging


DATABASE_URI = 'sqlite:////Users/borislavvoytash/Desktop/repos/etl_app/news_scraper/news_scraper/news.db'


engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


app = FastAPI()


# Dependency to get SQLAlchemy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# SQLAlchemy Model
class NewsArticle(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    url = Column(String, unique=True, index=True)
    author = Column(String)
    publication_date = Column(DateTime)
    image_urls = Column(String)
    body = Column(Text)
    ner_entities = Column(Text)


Base.metadata.create_all(bind=engine)


class NewsArticleResponse(BaseModel):
    id: int
    title: str
    url: str
    author: str
    publication_date: Optional[datetime]
    image_urls: str
    body: str
    ner_entities: str


class ArticleUpdate(BaseModel):
    title: Optional[str]
    url: Optional[str]
    author: Optional[str]
    publication_date: Optional[datetime]
    image_urls: Optional[str]
    body: Optional[str]
    ner_entities: Optional[str]


# Convert SQLAlchemy NewsArticle instance to Pydantic NewsArticleResponse
def convert_to_response(article: NewsArticle) -> NewsArticleResponse:
    return NewsArticleResponse(
        id=article.id,
        title=article.title,
        url=article.url,
        author=article.author,
        publication_date=article.publication_date,
        image_urls=article.image_urls,
        body=article.body,
        ner_entities=article.ner_entities
    )


@app.get('/articles/{article_id}', response_model=NewsArticleResponse)
def read_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")

    return NewsArticleResponse(
        id=article.id,
        title=article.title,
        url=article.url,
        author=article.author,
        publication_date=article.publication_date,
        image_urls=article.image_urls,
        body=article.body,
        ner_entities=article.ner_entities
    )


@app.delete('/articles/{article_id}', response_model=NewsArticleResponse)
def delete_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(article)
    db.commit()
    return convert_to_response(article)


@app.get('/articles/last', response_model=NewsArticleResponse)
def get_last_article(db: Session = Depends(get_db)):
    #article = db.query(NewsArticle).order_by(NewsArticle.id.desc()).first()
    article = session.query(NewsArticle).order_by(NewsArticle.id.desc()).first()
    if article is None:
        raise HTTPException(status_code=404, detail="No articles found")
    return convert_to_response(article)



@app.get('/articles/', response_model=List[NewsArticleResponse])
def get_articles_by_date_or_author(date: Optional[datetime] = None, author: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(NewsArticle)

    if date:
        query = query.filter(func.date(NewsArticle.publication_date) == date.date())
    if author:
        query = query.filter(NewsArticle.author == author)

    articles = query.all()
    return [convert_to_response(article) for article in articles]


@app.put('/article/{article_UID}')
def update_article(article_UID: int, article_update: ArticleUpdate, db: Session = Depends(get_db)):
    # Retrieve the article from the database
    article = db.query(NewsArticle).filter(NewsArticle.id == article_UID).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")

    # Update article attributes based on the request body
    for attr, value in article_update.dict(exclude_unset=True).items():
        setattr(article, attr, value)

    db.commit()
    return {"message": "Article updated successfully"}


if __name__ == "__main__":
    # http://127.0.0.1:8000/docs
    uvicorn.run(app, host="127.0.0.1", port=8000)