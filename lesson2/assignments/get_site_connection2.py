# coding=utf-8
# 抓取baike上的地铁站点连接信息，按照每条线路逐条获取，降低复杂度
import requests
from bs4 import BeautifulSoup
import re

base_url = "https://baike.baidu.com"
root_href = "/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%81/408485"


# 从百度百科获取站点Table，返回BeautifulSoup
def get_table_from_baike(href):
    kv = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0"}
    try:
        r = requests.get(base_url+href, headers = kv, allow_redirects=False)
    except:
        print('访问', href, '失败，重试')
        return get_table_from_baike(href)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, 'lxml')
    return soup.find_all("table")

print(get_table_from_baike(root_href))