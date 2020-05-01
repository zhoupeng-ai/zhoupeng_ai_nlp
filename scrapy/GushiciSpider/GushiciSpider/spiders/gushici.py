# -*- coding: utf-8 -*-
import scrapy
from GushiciSpider.items import GushicispiderItem

class GushiciSpider(scrapy.Spider):
    name = 'gushici'
    allowed_domains = ['www.gushicimingju.com']
    id = 1
    start_urls = ['http://www.gushicimingju.com/shiju/']


    def parse(self, response):
        for gushi_class_info in response.xpath('//div[@class="main-content gushi-info"][1]/ul[1]/li'):
            poem_class_href = gushi_class_info.xpath('./a/@href').extract_first()
            poem_class = gushi_class_info.xpath('./a/text()').extract_first()
            print("当前诗句类别:{0}".format(poem_class))
            yield scrapy.Request(url="http://www.gushicimingju.com" + poem_class_href,
                                 meta={'poem_class': poem_class,
                                       'poem_class_href': poem_class_href},
                                 callback=self.middle_parse)

    def middle_parse(self, response):
        poem_class_href = response.meta['poem_class_href']
        poem_class = response.meta['poem_class']
        for mingju_info in response.xpath('//ul[@class="good-mingju main-data"]/li'):
            detail_info_href = mingju_info.xpath('./span[last()]/a/@href').extract_first()
            if detail_info_href is None:
                continue
            poem_id = detail_info_href.split("/")[-1].split(".")[0]
            current_id = mingju_info.xpath('./span[1]/text()').extract_first().split(".")[0]
            # if response.xpath('//ul[@class="good-mingju main-data"]/li[@class="visible-xs visible-sm mobile-middle-good"]') \
            #         or response.xpath('//ul[@class="good-mingju main-data"]/li[@class="visible-md visible-lg hide-xs hide-sm"]'):
            #     continue
            print("当前类别：{0}".format(poem_class))
            print("当前类路径：{0}".format(poem_class_href))
            yield scrapy.Request(url="http://www.gushicimingju.com" + detail_info_href,
                                 meta={'poem_class': poem_class,
                                       "poem_id": poem_id,
                                       'detail_info_href': detail_info_href,
                                       'poem_class_href': poem_class_href},
                                 callback=self.detail_parse)

            if int(current_id) % 50 == 0:
                next_page = int(int(current_id) / 50 + 1)
                print("当前页:{0}, 下一页：{1}".format(next_page - 1, next_page))
                yield scrapy.Request(url="http://www.gushicimingju.com" + poem_class_href + str(next_page),
                                     callback=self.middle_parse)

    def detail_parse(self, response):
        item = GushicispiderItem()
        poem_class = response.meta['poem_class']
        poem_id = response.meta['poem_id']
        detail_info_href = response.meta['detail_info_href']
        poem_class_href = response.meta['poem_class_href']
        for gushi_info in response.xpath('//div[@class="main-content gushi-info"]'):
            poem_name = gushi_info.xpath('./h1/text()').extract_first()
            if poem_name is None:
                continue
            print("当前类别：{0}".format(poem_class))
            print("当前类路径：{0}".format(poem_class_href))
            print("当前诗路径：{0}".format(detail_info_href))
            print("当前诗名：{0}".format(poem_name))
            item['poem_name'] = poem_name
            item['poem_id'] = poem_class_href.split("/")[-2] + "_" + poem_id
            item['poem_class'] = poem_class
            for author_simple_info in gushi_info.xpath('./div[@class="author-simple-info"]/span'):
                if author_simple_info.xpath('./text()').extract_first() == '朝代：':
                    item['poet_dynasty'] = author_simple_info.xpath('./a/text()').extract_first()
                if author_simple_info.xpath('./text()').extract_first() == '作者：':
                    item['poet'] = author_simple_info.xpath('./a/text()').extract_first()
                else:
                    continue
            poem = gushi_info.xpath('./div[@class="shici-content"]')[0].xpath('string(.)').extract_first()

            item['poem'] = poem.replace("\n","").replace("\r", "").strip()
            yield scrapy.Request(url="http://www.gushicimingju.com" + detail_info_href,
                                 callback=self.detail_parse)
            yield item