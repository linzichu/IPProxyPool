from bs4 import BeautifulSoup
import requests

urls = ['https://www.yrw.com/products/list-direct-all-performance-1-createTimeDesc-{}.html'.format(str(i)) for i in
        range(1, 11)]


# print(urls)

def get_titles(urls, data=None):
    web_data = requests.get(urls)
    soup = BeautifulSoup(web_data.text, 'lxml')
    titles = soup.select(' h3 > a > em > strong')
    for title in titles:
        data = {
            'title': title.get_text()
        }
        print(data)


for titles in urls:
    get_titles(titles)
