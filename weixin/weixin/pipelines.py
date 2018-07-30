# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class WXGZPipeline(object):

    def open_spider(self, spider):
        # 创建一个mongo客户端对象
        client = MongoClient()
        # 创建一个集合保存数据
        self.collection = client["spider"]["wxgz"]

    def process_item(self, item, spider):
        if spider.name == "wxgz":
            self.collection.insert(item)
            print("保存成功")

        return item
