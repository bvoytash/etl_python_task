from datetime import datetime
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import sessionmaker
from .models import engine, Base, NewsArticle
from itemadapter import ItemAdapter
import json


class NewsScraperPipeline:
    def open_spider(self, spider):
        Base.metadata.create_all(bind=engine)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Convert item data to NewsArticle object
        article = NewsArticle(
            title=adapter.get('title'),
            url=adapter.get('url'),
            author=adapter.get('author'),
            publication_date=datetime.strptime(adapter.get('publication_date'), '%Y-%m-%d'),
            image_urls=', '.join(adapter.get('image_urls', [])),
            body='\n'.join(adapter.get('body', [])),
            ner_entities=json.dumps(adapter.get('ner_entities', [])),
        )

        try:
            # Check if the URL already exists in the database
            existing_article = self.session.query(NewsArticle).filter_by(url=article.url).one_or_none()
            if existing_article:
                spider.logger.info(f"Duplicate found: {article.url}")
                return item

            # Add the new article if URL does not exist
            self.session.add(article)
            self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
            spider.logger.error(f"IntegrityError on {article.url}: {e}")
        except Exception as e:
            self.session.rollback()
            spider.logger.error(f"Error processing item {article.url}: {e}")

        return item

    # def open_spider(self, spider):
    #     self.connection = sqlite3.connect('/Users/borislavvoytash/Desktop/repos/etl_app/news_scraper/news_scraper/news.db')
    #     self.cursor = self.connection.cursor()
    #     self.cursor.execute('''
    #         CREATE TABLE IF NOT EXISTS articles (
    #             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #             title TEXT,
    #             url TEXT,
    #             author TEXT,
    #             publication_date TEXT,
    #             image_urls TEXT,
    #             body TEXT,
    #             ner_entities TEXT
    #         )
    #     ''')
    #     self.connection.commit()
    #
    # def process_item(self, item, spider):
    #     self.cursor.execute('''
    #         INSERT INTO "articles" (title, url, author, publication_date, image_urls, body, ner_entities)
    #         VALUES (?, ?, ?, ?, ?, ?, ?)
    #     ''', (
    #         item['title'],
    #         item['url'],
    #         item['author'],
    #         item['publication_date'],
    #         item['image_urls'],
    #         ','.join(item['body']),
    #         # ','.join([f'{entity[0]} ({entity[1]})' for entity in item['ner_entities']]),
    #         json.dumps(item.get('ner_entities', []))
    #     ))
    #     self.connection.commit()
    #     return item
    #
    # def close_spider(self, spider):
    #     self.connection.close()