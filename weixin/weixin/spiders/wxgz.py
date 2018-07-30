# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
import time



class WxgzSpider(RedisSpider):
    name = 'wxgz'
    allowed_domains = ['weixin.qq.com']
    current = 0
    # start_urls = ['https://mp.weixin.qq.com/cgi-bin/appmsg?token=900493342&action=list_ex&begin=0&type=9&fakeid=MjM5NzU0MzU0Nw==']
    redis_key = "wxgz"

    def parse(self, response):
        page_dict = eval(response.body.decode())

        # print(page_dict)
        msg_list = page_dict["app_msg_list"]
        for msg in msg_list:
            item = {}
            item["title"] = msg["title"]
            item["url"] = msg["link"]

            if item["url"]:
                yield scrapy.Request(
                    url=item["url"],
                    callback=self.parse_detail,
                    meta={"item":item}
                )

        # 下一页url
        next_url = "https://mp.weixin.qq.com/cgi-bin/appmsg?token=900493342&action=list_ex&begin={}&type=9&fakeid=MjM5NzU0MzU0Nw=="
        total = page_dict["app_msg_cnt"]
        if self.current < total:
            self.current += 5
            next_url = next_url.format(self.current)
            time.sleep(1)
            print(next_url)

            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
                dont_filter=True

            )

    # 详情页
    def parse_detail(self,response):
        item = response.meta["item"]

        content = response.xpath("//div[@id='js_content']//text()").extract()
        item["content"] = [i.strip() for i in content if i.strip()]

        item["img"] = response.xpath("//div[@id='js_content']//img/@data-src").extract()

        yield item
























