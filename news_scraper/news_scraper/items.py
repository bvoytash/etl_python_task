# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsScraperItem(scrapy.Item):
    title = scrapy.Field()
    body = scrapy.Field()
    url = scrapy.Field()
    publication_date = scrapy.Field()
    author = scrapy.Field()
    image_urls = scrapy.Field()
    ner_entities = scrapy.Field()
