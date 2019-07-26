# coding=utf-8
# 可视化地铁图及完成路径搜索
import networkx as nx
import matplotlib.pyplot as plt

subway_sites_file = open("./subway_sites.txt", "r", encoding="utf8")
sites_coordinate_file = open("./sites_coordinate.txt", "r", encoding="utf8")

sites_connection = {}
sites_coordinate = {}

# 读取站点坐标
while True:
    line = sites_coordinate_file.readline()
    if not line:
        break
    site_name, lng, lat = line.replace('\n', '').split(",")
    sites_coordinate[site_name] = (float(lng), float(lat))


# 读取站点关系
while True:
    line = subway_sites_file.readline()
    if not line:
        break
    sites = line.replace('\n', '').split(",")
    print(sites[0])
    for i in range(1, len(sites)):
        if sites[i] not in sites_connection:
            sites_connection[sites[i]] = set()
        if i > 1:
            sites_connection[sites[i]].add(sites[i-1])
        if i < len(sites)-1:
            sites_connection[sites[i]].add(sites[i+1])

subway_sites_file.close()
sites_coordinate_file.close()

sites_gragh = nx.Graph(sites_connection)
nx.draw(sites_gragh, sites_coordinate, with_labels=True, node_size=12, font_family='YouYuan', font_size=7)
plt.show()

# 还是很丑,因该是nx对应方法和参数问题,回头再研究,先写搜索方法
