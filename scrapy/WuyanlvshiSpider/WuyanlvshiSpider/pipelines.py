# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

class WuyanlvshispiderPipeline:
    def __init__(self):
        self.json_file = open("wuyanlvshi.json", "wb+")
        print("----------开始写入文件-------------")
        self.json_file.write('[\n'.encode("utf-8"))

    def close_spider(self, spider):
        print("----------关闭文件-------------")
        self.json_file.seek(-2, 1)
        self.json_file.write('\n]'.encode("utf-8"))
        self.json_file.close()

    def process_item(self, item, spider):
        text = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.json_file.write(text.encode("utf-8"))
