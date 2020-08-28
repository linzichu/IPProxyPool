import requests
from lxml import etree
from utils import http
from domain import Proxy

url = "https://www.kuaidaili.com/free/inha/1/"

html = requests.get(url, headers=http.get_headers()).content
Music = etree.HTML(html)
trs = Music.xpath('//*[@id="list"]/table/tbody/tr')

for tr in trs:
    ip = Music.xpath('//*[@id="list"]/table/tbody/tr[1]/td[1]/text()')
    port = Music.xpath('//*[@id="list"]/table/tbody/tr[1]/td[2]/text()')
    area = Music.xpath('//*[@id="list"]/table/tbody/tr[1]/td[5]/text()')
    proxy = Proxy(ip, port, area=area)
    # 使用yield返回提取到的数据
    print(proxy)
