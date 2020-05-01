# -*- coding: utf-8 -*-
import scrapy
from XiyoujiSpider.items import XiyoujispiderItem

class XiyoujiSpider(scrapy.Spider):
    name = 'xiyouji'
    allowed_domains = ['http://www.eywedu.com/Xiyou/01/mydoc001.htm']
    start_urls = ['http://www.eywedu.com/Xiyou/01/mydoc001.htm/']

    def parse(self, response):
        print(response)
        pass
