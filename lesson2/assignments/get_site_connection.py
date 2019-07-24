# coding=utf-8
# 抓取baike上的地铁站点连接信息
import requests
from bs4 import BeautifulSoup
import re

base_url = "https://baike.baidu.com"
root_href = "/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%81/408485"

# [(根站点, 站点href)]
sites_href = []

# 已经访问过的页面href
href_seen = {}


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
    return soup.find_all('table')


file = open('./sites_connection.txt', 'w')
# 获取所有线路(23)的起始站点或者回库站点的名称及URL
# 这种方法经验证，会丢失站点关系，决定换个方法来
metro_lines = get_table_from_baike(root_href)[1]
for line in metro_lines.contents[1:-1]:
    # site_content = line.contents[4]
    # print(site_content)
    for site_td in line:
        if not site_td.a:
            continue
        td_sites = site_td.find_all('a')
        for td_site in td_sites:
            if td_site.text not in sites_href:
                sites_href.append((td_site.text, td_site['href']))
# print(sites_connection)
# print(sites_href)

nex_site_pattern = re.compile(r"（下一站：<a.*href=\"(.*)\" target=\"_blank\".*>(.*)</a>）")

# 从sites_href元组作为根节点，BFS抓取站点信息
while sites_href:
    name, href = sites_href.pop(0)
    if href in href_seen:
        continue
    print(name, base_url + href)
    next_site_talbes = get_table_from_baike(href)
    href_seen[href] = name
    for next_site_trs in next_site_talbes:
        for next_site_div in next_site_trs.contents:
            # print(str(next_site_div))
            results = nex_site_pattern.findall(str(next_site_div))
            if results:
                for site_info in results:
                    next_href, next_name = site_info
                    sites_href.append((next_name, next_href))
                    file.write("%s,%s\n"%(name, next_name))
file.close()

