# coding=utf-8
# 可视化地铁图及完成路径搜索
import networkx as nx
import matplotlib.pyplot as plt

sites_connection_file = open("./sites_connection.txt", "r")
sites_coordinate_file = open("./sites_coordinate.txt", "r")

sites_connection = {}
sites_coordinate = {}
# 读取站点关系
while True:
    line = sites_connection_file.readline()
    if not line:
        break
    site1, site2 = line.replace('\n', '').split(",")
    if site1 in sites_connection:
        if site2 not in sites_connection[site1]:
            sites_connection[site1].append(site2)
    else:
        sites_connection[site1] = [site2]

# 读取站点坐标
while True:
    line = sites_coordinate_file.readline()
    if not line:
        break
    site_name, lng, lat = line.replace('\n', '').split(",")
    sites_coordinate[site_name] = (float(lng), float(lat))
    print(sites_coordinate[site_name])

print(sites_connection)
print(sites_coordinate)

sites_connection_file.close()
sites_coordinate_file.close()

sites_gragh = nx.Graph(sites_connection)
nx.draw(sites_gragh, with_labels=True, node_size=10, font_family='YouYuan', font_size=8)
plt.show()