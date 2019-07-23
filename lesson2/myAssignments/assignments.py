# coding=utf-8
import requests
from bs4 import BeautifulSoup
import re

base_url = "https://baike.baidu.com"
root_href = "/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%81/408485"

# 站点间连接的集合
sites_connection = {}
# [(根站点, 站点href)]
sites_href = []
# 站点经纬度
sites_situation = {}
# 已经访问过的页面href
href_seen = {}


# 从百度百科获取站点Table，返回BeautifulSoup
def get_table_from_baike(href):
    kv = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0"}
    r = requests.get(base_url+href, headers = kv, allow_redirects=False)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, 'lxml')
    return soup.find_all('table')


# 获取所有线路(23)的起始站点或者回库站点的名称及URL
metro_lines = get_table_from_baike(root_href)[1]
for line in metro_lines.contents[1:-1]:
    # site_content = line.contents[4]
    # print(site_content)
    for site_td in line:
        if not site_td.a:
            continue
        td_sites = site_td.find_all('a')
        for td_site in td_sites:
            if td_site.text not in sites_connection:
                sites_connection[td_site.text] = []
            if td_site.text not in sites_href:
                sites_href.append((td_site.text, td_site['href']))
print(sites_connection)
print(sites_href)

# 从sites_href元组作为根节点，BFS抓取站点信息
# while sites_href:
site_name, site_href = sites_href.pop()
# if site_href in href_seen:
#     continue
metro_site = get_table_from_baike(site_href)[0]
for line in metro_site.contents:
    print(line)
