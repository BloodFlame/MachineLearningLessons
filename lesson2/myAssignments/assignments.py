# coding=utf-8
import requests
from bs4 import BeautifulSoup

kv = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0"}
r = requests.get('https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%81/408485', headers = kv, allow_redirects=False)
r.encoding = "utf-8"
soup = BeautifulSoup(r.text)
print(soup.prettify())