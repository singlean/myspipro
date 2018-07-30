# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from queue import Queue

class MZTPipeline(object):

    def process_item(self, item, spider):
        if spider.name == "mzt":
            with open("./picture/{}/{}/{}.jpg".format(item["type_one"], item["group_map_title"], item["img_name"]),
                      "wb") as f:
                f.write(item["img_content"])
                print(item["group_map_href"],item["img_name"])
        return item


class ZSPipeline(object):

    def process_item(self, item, spider):
        if spider.name == "zs":
            with open("./picture/{}/{}/{}.jpg".format("全裸", item["group_map_title"], item["img_name"]),
                      "wb") as f:
                f.write(item["img_content"])
                print(item["group_map_title"],item["img_name"])
        return item

















