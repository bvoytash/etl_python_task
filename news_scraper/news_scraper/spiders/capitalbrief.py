# import scrapy
#
# from news_scraper.news_scraper.items import NewsScraperItem
#
#
# class CapitalbriefSpider(scrapy.Spider):
#     name = 'capitalbrief'
#     allowed_domains = ['capitalbrief.com']
#     start_urls = ['https://www.capitalbrief.com/technology/']
#
#     def parse(self, response):
#         articles = response.xpath("//article")
#         for article in articles:
#             pass
#
#     def parse_article(self, response):
#         pass
