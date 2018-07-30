# -*- coding: utf-8 -*-
import scrapy,os
from copy import deepcopy
from urllib.parse import urljoin
from scrapy_redis.spiders import RedisSpider
from queue import Queue


class MztSpider(RedisSpider):
    name = 'mzt'
    allowed_domains = ['meizitu.com',"chinasareview.com"]
    # start_urls = ['http://www.meizitu.com/']
    redis_key = "mzt"


    def parse(self, response):

        # 分类列表
        a_list = response.xpath("//div[@id='container']//div[@class='tags']/span/a")
        for a in a_list:
            item = {}
            item["type_one"] = a.xpath("./text()").extract_first()
            item["type_href"] = a.xpath("./@href").extract_first()

            # 创建多层目录、以创建就跳过
            try:
                os.makedirs("./picture/{}".format(item["type_one"]))
            except:
                pass
            if item["type_href"]:

                yield scrapy.Request(
                    url=item["type_href"],
                    callback=self.parse_list_one,
                    meta={"item":item},
                    dont_filter=True
                )

    def parse_list_one(self,response):
        item = response.meta["item"]

        # 组图列表
        li_list = response.xpath("//div[@class='inWrap']/ul/li")
        for li in li_list:
            item["group_map_href"] = li.xpath(".//h3/a/@href").extract_first()
            item["group_map_title"] = li.xpath(".//h3/a//text()").extract_first()

            # 创建多层目录、以创建就跳过
            try:
                os.makedirs("./picture/{}/{}".format(item["type_one"], item["group_map_title"]))
            except:
                pass

            print(item)
            if item["group_map_href"]:

                yield scrapy.Request(
                    url=item["group_map_href"],
                    callback=self.parse_detail,
                    meta={"item":deepcopy(item)}
                )

        # next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        # if next_url:
        #     next_url = urljoin(response.url,next_url)
        #     print("分页",next_url)
        #
        #     yield scrapy.Request(
        #         url=next_url,
        #         callback=self.parse_list_one,
        #         meta={"item":item},
        #         dont_filter=True
        #     )

    def parse_detail(self,response):
        item = response.meta["item"]

        # 图片列表
        img_list = response.xpath("//div[@id='picture']/p/img")
        for img in img_list:
            item["img_url"] = img.xpath("./@src").extract_first()
            item["img_name"] = img.xpath("./@alt").extract_first().split("，")[0] + "第{}张".format(img_list.index(img))

            if item["img_url"]:
                yield scrapy.Request(
                    url=item["img_url"],
                    callback=self.parse_img,
                    meta={"item":deepcopy(item)}
                )

    def parse_img(self,response):
        item = response.meta["item"]
        item["img_content"] = response.body

        # with open("./picture/{}/{}/{}.jpg".format(item["type_one"], item["group_map_title"], item["img_name"]),
        #           "wb") as f:
        #     f.write(item["img_content"])
        #     print(item["group_map_href"])

        yield deepcopy(item)

















