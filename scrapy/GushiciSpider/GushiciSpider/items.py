# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GushicispiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    poet = scrapy.Field()
    poet_dynasty = scrapy.Field()
    poem = scrapy.Field()
    poem_id = scrapy.Field()
    poem_name = scrapy.Field()
    poem_class = scrapy.Field()
    pass
