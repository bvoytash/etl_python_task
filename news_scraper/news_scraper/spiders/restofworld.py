import scrapy
from datetime import datetime
from ..items import NewsScraperItem
import spacy
nlp = spacy.load("en_core_web_sm")


class RestOfWorldSpider(scrapy.Spider):
    name = "restofworld"
    allowed_domains = ["restofworld.org"]
    start_urls = ["https://restofworld.org/"]

    def parse(self, response):
        articles = response.xpath("//article")

        for article in articles:
            title = article.xpath('.//a/h4/text()').get()
            url = article.xpath('.//a/@href').get()
            if not title:
                continue
            yield response.follow(url, self.parse_article, meta={'title': title})

    def parse_article(self, response):
        title = response.meta['title']
        publication_date = response.xpath('.//time/@datetime').get()
        body = response.xpath('//div[@class="post-content"]//p/text()').getall()
        author = response.xpath('//*[@rel="author"]/text()').get()
        image_urls = response.xpath('//div[@class="post-content"]//img/@src').getall()

        # image_urls_str = ' '.join(image_urls) if image_urls else ''
        article_text = ' '.join(body)
        ner_entities = perform_ner(article_text)

        item = NewsScraperItem()
        item['title'] = title
        item['url'] = response.url
        item['author'] = author
        item['publication_date'] = publication_date
        item['image_urls'] = image_urls
        item['body'] = body
        item['ner_entities'] = ner_entities

        yield item


def perform_ner(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))
    return entities