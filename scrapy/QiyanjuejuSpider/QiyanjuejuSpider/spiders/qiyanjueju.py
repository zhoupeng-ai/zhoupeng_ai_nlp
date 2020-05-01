# -*- coding: utf-8 -*-
import scrapy
from QiyanjuejuSpider.items import QiyanjuejuspiderItem


class QiyanjuejuSpider(scrapy.Spider):
    name = 'qiyanjueju'
    allowed_domains = ['www.gushicimingju.com']
    start_urls = ['http://www.gushicimingju.com/gushi/qiyanjueju/']

    def parse(self, response):
        for simple_shiciqu in response.xpath('//ul[@class="simple-shiciqu has-author main-data"]/li[not(@class="visible-xs visible-sm mobile-middle-good" or @class="md visible-md visible-lg")]'):
            item = QiyanjuejuspiderItem()
            item['name'] = simple_shiciqu.xpath('./a/text()').extract_first()
            id = simple_shiciqu.xpath('./text()').extract_first().split('.')[0]
            print(id)
            item['id'] = id
            item['dynasty'] = simple_shiciqu.xpath('./a')[1].xpath('./text()').extract_first()
            if simple_shiciqu.xpath('./a[@class="author"]'):
                author = simple_shiciqu.xpath('./a[@class="author"]/text()').extract_first()
            else:
                author = "未知"

            item['author'] = author

            item['verse'] = simple_shiciqu.xpath('./span[@class="content"]/text()').extract_first()

            item['verse_class'] = '七言绝句'
            if int(id) % 20 == 0:
                next_page = int(int(id)/20 + 1)
                print("当前页:{0}, 下一页：{1}".format(next_page-1, next_page))
                yield scrapy.Request(url="http://www.gushicimingju.com/gushi/qiyanjueju/page" + str(next_page) + "/",
                                     callback=self.parse)
            yield item
