# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class BookItem(scrapy.Item):
    data_sku = Field()
    name = Field()
    author = Field()
    price = Field()
    publishing_house = Field()
    date = Field()
    comments_count = Field()

