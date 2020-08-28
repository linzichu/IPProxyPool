import requests
from utils import http
from lxml import etree
from domain import Proxy


# 1.在base_spider文件中，定义一个BaseSpider类，继承object类
class BaseSpider(object):
    # 2.提供三个类成员变量
    # urls：代理网址的URL列表
    urls = []
    # group_xpath：分组Xpath，获取包含代理IP信息标签列表的xpath
    group_xpath = ''
    # detail_xpath：组内xpath，获取代理IP详情的信息XPATH
    detail_xpath = {}

    def __init__(self, urls=[], group_xpath='', detail_xpath={}):
        if urls:
            self.urls = urls
        if group_xpath:
            self.group_xpath = group_xpath
        if detail_xpath:
            self.detail_xpath = detail_xpath

    def get_page_from_url(self, url, headers=http.get_headers()):
        """根据发送url请求，获取页面数据"""
        print(url)
        response = requests.get(url, headers)
        return response.content

    def get_proxies_from_page(self, page):
        """解析页面，提取数据，封装为Proxy对象"""
        element = etree.HTML(page)
        print(element)
        # 获取包含代理IP信息的标签列表
        trs = element.xpath(self.group_xpath)
        print(trs)
        # 遍历trs，获取代理ip相关信息
        for tr in trs:
            # 解析出的是一个list，加上[0]给变量赋值列表的值
            ip = tr.xpath(self.detail_xpath['ip'])[0]
            port = tr.xpath(self.detail_xpath['port'])[0]
            area = tr.xpath(self.detail_xpath['area'])[0]
            proxy = Proxy(ip, port, area=area)
            # 使用yield返回提取到的数据
            yield proxy

    def get_proxies(self):
        # 4.对外提供一个获取代理Ip的方法
        # 4.1遍历url列表，获取URL
        for url in self.urls:
            # 4.2根据发送请求，获取页面数据
            page = self.get_page_from_url(url)
            # 4.3解析页面，提取数据，封装为Proxy对象
            print(page)
            proxies = self.get_proxies_from_page(page)
            # 4.4返回Proxy对象列表
            yield from proxies


if __name__ == '__main__':
    config = {
        'urls': ['https://www.kuaidaili.com/free/inha/{}/'.format(i) for i in range(1, 5)],
        'group_xpath': '//*[@id="list"]/table/tbody/tr',
        'detail_xpath': {
            'ip': './td[1]/text()',
            'port': './td[2]/text()',
            'area': './td[5]/text()'
        }
    }
    spider = BaseSpider(**config)

    for i in spider.get_proxies():
        print(i)
