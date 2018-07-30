import requests,os
from queue import Queue
from fake_useragent import UserAgent
from lxml import etree
from threading import Thread
from copy import deepcopy
import time,random
from urllib.parse import urljoin


class MZTSpider:

    def __init__(self):
        self.list_one_item_queue = Queue()
        self.type_page_item_queue = Queue()
        self.detail_page_item_queue = Queue()
        self.img_item_queue = Queue()
        self.user_agent = UserAgent()
        self.headers = {
            "User-Agent":self.user_agent.chrome,
            "Host": "www.meizitu.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
                        }
        self.start_urls = "http://www.meizitu.com/"

    # 获取响应，返回etree对象
    def get_html(self,url):
        # 随机延迟
        if random.randint(0,4) == 0:
            delay = random.random()
        else:
            delay = 0
        time.sleep(delay)
        html = requests.get(url,headers=self.headers)
        return etree.HTML(html.content.decode("gbk"))

    # 获取首页分类列表
    def get_list_one(self):
        str_html = self.get_html(self.start_urls)
        list_one_html = str_html.xpath("//div[@id='container']//div[@class='tags']/span/a")
        for one in list_one_html:
            item = {}
            item["type_one"] = one.xpath("./text()")[0]
            item["type_href"] = one.xpath("./@href")[0]
            self.list_one_item_queue.put(item)

    # 获取分类页面组图
    def get_type_page(self):
        while True:
            item = self.list_one_item_queue.get()
            url = item["type_href"]
            str_html = self.get_html(url)
            group_pic_list = str_html.xpath("//div[@class='inWrap']/ul/li")
            for pic in group_pic_list:
                item["group_map_href"] = pic.xpath(".//h3/a/@href")[0]
                item["group_map_title"] = pic.xpath(".//h3/a//text()")[0]
                self.type_page_item_queue.put(deepcopy(item))
            self.list_one_item_queue.task_done()

            next_url = str_html.xpath("//a[text()='下一页']/@href")
            if next_url:
                item["type_href"] = urljoin(item["type_href"],next_url[0])
                self.list_one_item_queue.put(deepcopy(item))

    # 获取组图页面
    def get_detail_page(self):
        while True:
            item = self.type_page_item_queue.get()
            url = item["group_map_href"]
            str_html = self.get_html(url)
            img_list = str_html.xpath("//div[@id='picture']/p/img")
            for img in img_list:
                item["img_url"] = img.xpath("./@src")[0]
                item["img_name"] = img.xpath("./@alt")[0].split("，")[0] + "第{}张".format(img_list.index(img))
                self.detail_page_item_queue.put(deepcopy(item))
            self.type_page_item_queue.task_done()

    # 获取图片
    def get_img(self):
        while True:
            item = self.detail_page_item_queue.get()
            # 随机延迟
            if random.randint(0,4) == 0:
                delay = random.random()
            else:
                delay = 0
            time.sleep(delay)
            html = requests.get(item["img_url"],headers=self.headers)
            item["content"] = html.content
            self.img_item_queue.put(deepcopy(item))
            self.detail_page_item_queue.task_done()

    # 保存图片
    def save_img(self):
        while True:
            item = self.img_item_queue.get()
            try:
                os.makedirs("./pic/{}/{}".format(item["type_one"], item["group_map_title"]))
            except:
                pass
            with open("./pic/{}/{}/{}.jpg".format(item["type_one"], item["group_map_title"],item["img_name"]),"wb") as f:
                f.write(item["content"])
                print(item["type_one"],item["group_map_title"],item["img_name"],item["group_map_href"])
            self.img_item_queue.task_done()

    def run(self):

        self.get_list_one()
        t_list = []
        for i in range(3):
            t_type_page = Thread(target=self.get_type_page)
            t_list.append(t_type_page)

        for i in range(3):
            t_detail_page = Thread(target=self.get_detail_page)
            t_list.append(t_detail_page)

        for i in range(4):
            t_img = Thread(target=self.get_img)
            t_list.append(t_img)

        for i in range(8):
            t_save = Thread(target=self.save_img)
            t_list.append(t_save)

        for t in t_list:
            t.setDaemon(True)
            t.start()

        for q in [self.list_one_item_queue,self.detail_page_item_queue,self.type_page_item_queue,self.img_item_queue]:
            q.join()

        print("程序结束")

mzt = MZTSpider()
mzt.run()





















