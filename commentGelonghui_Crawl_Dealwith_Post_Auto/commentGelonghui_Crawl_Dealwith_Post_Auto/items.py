# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CommentItem(scrapy.Item):
    comment = scrapy.Field()
    publishTime = scrapy.Field()
    url = scrapy.Field()
