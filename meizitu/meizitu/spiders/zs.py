# -*- coding: utf-8 -*-
import scrapy,os
from copy import deepcopy
from urllib.parse import urljoin


class ZsSpider(scrapy.Spider):
    name = 'zs'
    allowed_domains = ['meizitu.com',"chinasareview.com"]
    start_urls = ['http://www.meizitu.com/tag/quanluo_4_1.html']

    def parse(self, response):
        # 组图列表
        li_list = response.xpath("//div[@class='inWrap']/ul/li")
        for li in li_list:
            item = {}
            item["group_map_href"] = li.xpath(".//h3/a/@href").extract_first()
            item["group_map_title"] = li.xpath(".//h3/a//text()").extract_first()

            if item["group_map_href"]:
                # 创建多层目录、以创建就跳过
                try:
                    os.makedirs("./picture/{}/{}".format("全裸", item["group_map_title"]))
                except:
                    pass
                yield scrapy.Request(
                    url=item["group_map_href"],
                    callback=self.parse_detail,
                    meta={"item":item}
                )

            next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
            if next_url:
                next_url = urljoin(response.url,next_url)
                print("分页",next_url)

                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse
                )

    def parse_detail(self, response):
        item = response.meta["item"]

        # 图片列表
        img_list = response.xpath("//div[@id='picture']/p/img")
        for img in img_list:
            item["img_url"] = img.xpath("./@src").extract_first()
            item["img_name"] = img.xpath("./@alt").extract_first().split("，")[0] + "第{}张".format(
                img_list.index(img))

            if item["img_url"]:
                yield scrapy.Request(
                    url=item["img_url"],
                    callback=self.parse_img,
                    meta={"item": deepcopy(item)}
                )

    def parse_img(self, response):
        item = response.meta["item"]
        item["img_content"] = response.body

        with open("./picture/{}/{}/{}.jpg".format("全裸", item["group_map_title"], item["img_name"]),
                  "wb") as f:
            f.write(item["img_content"])
            print(item["group_map_title"], item["img_name"])

        # yield deepcopy(item)