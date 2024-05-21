# test_db.py
from datetime import datetime
from models import engine, Base, NewsArticle
from sqlalchemy.orm import sessionmaker

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

article = NewsArticle(
    title="New Title",
    url="http://example.com/second_example/boro",
    author="Test Author",
    publication_date=datetime.now(),
    image_urls="http://smotana-rabota.jpg",
    body="This is a test article.",
    ner_entities='{"entity": "test"}'
)

session.add(article)
session.commit()
session.close()
#
# articles = session.query(NewsArticle).all()
#
# # Display the articles
# for article in articles:
#     print(f"Title: {article.title}")
#     print(f"URL: {article.url}")
#     print(f"Author: {article.author}")
#     print(f"Publication Date: {article.publication_date}")
#     print(f"Image URLs: {article.image_urls}")
#     print(f"Body: {article.body}")
#     print(f"NER Entities: {article.ner_entities}")
#     print("-" * 80)