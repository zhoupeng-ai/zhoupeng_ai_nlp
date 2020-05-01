# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem


class TencentSpider(scrapy.Spider):
	# 爬虫名称
	name = 'tencent'
	# 允许爬取的域名
	allowed_domains = ['www.xxx.com']
	# 爬虫基础地址 用于爬虫域名的拼接
	base_url = 'https://www.xxx.com/'
	# 爬虫入口爬取地址
	start_urls = ['https://www.xxx.com/position.php']
	# 爬虫爬取页数控制初始值
	count = 1
	# 爬虫爬取页数 10为只爬取一页
	page_end = 1

	def parse(self, response):

		nodeList = response.xpath(
			"//table[@class='tablelist']/tr[@class='odd'] | //table[@class='tablelist']/tr[@class='even']")
		for node in nodeList:
			item = TencentItem()

			item['title'] = node.xpath("./td[1]/a/text()").extract()[0]
			if len(node.xpath("./td[2]/text()")):
				item['position'] = node.xpath("./td[2]/text()").extract()[0]
			else:
				item['position'] = ''
			item['num'] = node.xpath("./td[3]/text()").extract()[0]
			item['address'] = node.xpath("./td[4]/text()").extract()[0]
			item['time'] = node.xpath("./td[5]/text()").extract()[0]
			item['url'] = self.base_url + node.xpath("./td[1]/a/@href").extract()[0]
			# 根据内页地址爬取
			yield scrapy.Request(item['url'], meta={'item': item}, callback=self.detail_parse)

		# 有下级页面爬取 注释掉数据返回
		# yield item

		# 循环爬取翻页
		nextPage = response.xpath("//a[@id='next']/@href").extract()[0]
		# 爬取页数控制及末页控制
		if self.count < self.page_end and nextPage != 'javascript:;':
			if nextPage is not None:
				# 爬取页数控制值自增
				self.count = self.count + 1
				# 翻页请求
				yield scrapy.Request(self.base_url + nextPage, callback=self.parse)
		else:
			# 爬虫结束
			return None

	def detail_parse(self, response):
		# 接收上级已爬取的数据
		item = response.meta['item']
		# 一级内页数据提取
		item['zhize'] = \
		response.xpath("//*[@id='position_detail']/div/table/tr[3]/td/ul[1]").xpath('string(.)').extract()[0]
		item['yaoqiu'] = \
		response.xpath("//*[@id='position_detail']/div/table/tr[4]/td/ul[1]").xpath('string(.)').extract()[0]
		# 二级内页地址爬取
		yield scrapy.Request(item['url'] + "&123", meta={'item': item}, callback=self.detail_parse2)

	# 有下级页面爬取 注释掉数据返回
	# return item
	def detail_parse2(self, response):
		# 接收上级已爬取的数据
		item = response.meta['item']
		# 二级内页数据提取
		item['test'] = "111111111111111111"
		# 最终返回数据给爬虫引擎
		return item