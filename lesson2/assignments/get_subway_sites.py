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


soup_tables = get_table_from_baike(root_href)
soup_table = soup_tables[2]

subway_pattern = re.compile(r"北京地铁[\u4e00-\u9fa5a-zA-Z0-9]+线")
subway_hrefs = set()

# 保存下每一条线路的跳转路径
for soup_td in soup_table.find_all("td"):
    soup_a = soup_td.find_all("a", text=subway_pattern)
    for soup_a_link in soup_a:
        subway_name = soup_a_link.text
        subway_url = soup_a_link['href']
        subway_hrefs.add((subway_name, subway_url))

# 获取到19条线路(官称22条, 8和14号分段了)
subway_hrefs = list(subway_hrefs)
print(len(subway_hrefs))

# 逐条线路获取站点后保存
metro_pattern = re.compile(r"换乘线路")
metro_sites = {}

for subway_name, subway_href in subway_hrefs:
    soup_metro_tables = get_table_from_baike(subway_href)
    print(subway_name)
    metro_sites[subway_name] = []
    searched_table = None
    # 先确认table结构是想要的那一个,这里统一用“车站信息”表
    for soup_metro_table in soup_metro_tables:
        # descendants 是所有的子结构,如果包含"换乘线路"就是目标的表
        for soup_descendant in soup_metro_table.descendants:
            if not isinstance(soup_descendant, str):
                soup_find = soup_descendant.find_all(text=metro_pattern)
                if soup_find:
                    searched_table = soup_metro_table
                    break
    # 对目标表先取第一行tr(表头)看我们想要的名称是哪一列
    head_tr = searched_table.find('tr')
    site_name_index = 0
    # 这里会有两种情况,有的表子结构是td,有的是tr
    for head_td in head_tr.find_all('td'):
        if head_td.text == "车站名称":
            break
        site_name_index += 1
    for head_th in head_tr.find_all('th'):
        if head_th.text == "车站名称":
            break
        # 9号线的样式特殊,车站名称还做了单独样式，包含了一个div，特殊处理下
        if head_th.find('div') and head_th.find('div').text == '车站名称':
            break
        site_name_index += 1
    # 获取站点信息,跳过第一行表头
    site_trs = searched_table.find_all('tr')
    for site_tr in site_trs[1:]:
        # 子结构可能是th或者td
        site_tds = site_tr.find_all(re.compile(r"th|td"))
        if len(site_tds) > site_name_index:
            # 没有href的站点是未开通的站点
            if site_tds[site_name_index].find("a", href=True, text=True):
                metro_sites[subway_name].append(site_tds[site_name_index].text.replace('\n', ''))
pass

# 大功告成,保存好站点信息
file = open("./subway_sites.txt", "w", encoding="utf8")
for name in metro_sites:
    sites_str = ",".join(metro_sites[name])
    file.write("%s,%s\n"%(name, sites_str))
file.close()
