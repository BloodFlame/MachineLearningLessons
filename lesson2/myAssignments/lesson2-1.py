# 课堂代码复现
import re
import math
import networkx as nx
import matplotlib.pyplot as plt

coordination_source = '''
{name:'兰州', geoCoord:[103.73, 36.03]},
{name:'嘉峪关', geoCoord:[98.17, 39.47]},
{name:'西宁', geoCoord:[101.74, 36.56]},
{name:'成都', geoCoord:[104.06, 30.67]},
{name:'石家庄', geoCoord:[114.48, 38.03]},
{name:'拉萨', geoCoord:[102.73, 25.04]},
{name:'贵阳', geoCoord:[106.71, 26.57]},
{name:'武汉', geoCoord:[114.31, 30.52]},
{name:'郑州', geoCoord:[113.65, 34.76]},
{name:'济南', geoCoord:[117, 36.65]},
{name:'南京', geoCoord:[118.78, 32.04]},
{name:'合肥', geoCoord:[117.27, 31.86]},
{name:'杭州', geoCoord:[120.19, 30.26]},
{name:'南昌', geoCoord:[115.89, 28.68]},
{name:'福州', geoCoord:[119.3, 26.08]},
{name:'广州', geoCoord:[113.23, 23.16]},
{name:'长沙', geoCoord:[113, 28.21]},
{name:'海口', geoCoord:[110.35, 20.02]},
{name:'沈阳', geoCoord:[123.38, 41.8]},
{name:'长春', geoCoord:[125.35, 43.88]},
{name:'哈尔滨', geoCoord:[126.63, 45.75]},
{name:'太原', geoCoord:[112.53, 37.87]},
{name:'西安', geoCoord:[108.95, 34.27]},
{name:'台湾', geoCoord:[121.30, 25.03]},
{name:'北京', geoCoord:[116.46, 39.92]},
{name:'上海', geoCoord:[121.48, 31.22]},
{name:'重庆', geoCoord:[106.54, 29.59]},
{name:'天津', geoCoord:[117.2, 39.13]},
{name:'呼和浩特', geoCoord:[111.65, 40.82]},
{name:'南宁', geoCoord:[108.33, 22.84]},
//{name:'西藏', geoCoord:[91.11, 29.97]},
{name:'银川', geoCoord:[106.27, 38.47]},
{name:'乌鲁木齐', geoCoord:[87.68, 43.77]},
{name:'香港', geoCoord:[114.17, 22.28]},
{name:'澳门', geoCoord:[113.54, 22.19]}
'''
city_location = {}
pattern = re.compile(r"name:'(\w+)',\s+geoCoord:\[(\d+.\d+),\s+(\d+.\d+)\]")

for line in coordination_source.split('\n'):
    city_info = pattern.findall(line)
    if not city_info: continue
    city, long, lat = city_info[0]
    city_location[city] = (float(long), float(lat))

def geo_distance(origin, destination):
    long1, lat1 = origin
    long2, lat2 = destination
    radius = 6371
    #两地间弧度计算，经纬度也就是角度值
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(long2 - long1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius * c


def get_geo_distance(city1, city2):
    return geo_distance(city_location[city1], city_location[city2])


city_gragh = nx.Graph()
city_gragh.add_nodes_from(list(city_location.keys()))

# nx.draw(city_gragh, city_location,with_labels=True, node_size=10, font_family ='YouYuan', font_size = 11)
# plt.show()

"""
BFS 和 DFS
"""
simple_connection_info_src = {
    '北京': ['太原', '沈阳'],
    '太原': ['北京', '西安', '郑州'],
    '兰州': ['西安'],
    '郑州': ['太原', '福州'],
    '西安': ['兰州', '长沙', '太原'],
    '长沙': ['福州', '南宁', '西安'],
    '沈阳': ['北京'],
    '南宁': ['长沙'],
    '福州': ['长沙', '郑州']
}
# simple_connection_info_gragh = nx.Graph(simple_connection_info_src)
# nx.draw(simple_connection_info_gragh, city_location, with_labels=True, node_size=10, font_family='YouYuan', font_size=11)
# plt.show()

def bfs_search(start, end):
    pathes = [[start]]
    results = []
    print('BFS:',start,end='')
    while pathes:
        path = pathes.pop()
        if not path or path[-1] not in simple_connection_info_src:
            return results
        next_cities = simple_connection_info_src[path[-1]]
        for city in next_cities:
            if city in path:
                continue
            new_path = path + [city]
            print('->',city,end='')
            if city == end:
                results.append(new_path)
            else:
                pathes = pathes + [new_path]
    return results

# 递归来写很简单的，用遍历来写真的头大，但是运行效率好一些，没有大量栈帧回收的消耗和递归太深耗尽运行栈的问题
def dfs_search(start, end):
    stack = [start]
    path = []
    results = []
    pre_path_node = {}
    #记录每个城市遍历时在path中的上一个城市位置，在已经找到或者某路径尽头没有找到时回退path,由于是图
    # ，有可能多次遍历同一个点，使用一个list来保存，尾端是最新的一次遍历结果
    pre_path_node[start] = [0]
    print('DFS: ', end='')
    first_one = True
    while stack:
        cur_city = stack.pop()
        path = path[:pre_path_node[cur_city].pop()+1]
        if first_one:
            print(cur_city,end='')
            first_one = False
        else:
            print('->',cur_city,end='')
        path.append(cur_city)
        if cur_city == end:
            results.append(path.copy())
            continue
        if cur_city in simple_connection_info_src:
            next_cities = simple_connection_info_src[cur_city]
            new_cities = []
            for city in next_cities:
                if city in path:
                    continue
                new_cities.append(city)
                if city not in pre_path_node:
                    pre_path_node[city] = [len(path)-1]
                else:
                    pre_path_node[city].append(len(path)-1)
            if new_cities:
                stack = stack + new_cities
    return results

# print('\n', bfs_search('沈阳', '南宁'))
# print('\n', dfs_search('沈阳', '南宁'))
"""
BFS 和 DFS 路径比较
BFS: 沈阳-> 北京-> 太原-> 西安-> 郑州-> 福州-> 长沙-> 南宁-> 西安-> 兰州-> 兰州-> 长沙-> 福州-> 南宁-> 郑州
DFS: 沈阳-> 北京-> 太原-> 郑州-> 福州-> 长沙-> 西安-> 兰州-> 南宁-> 西安-> 长沙-> 南宁-> 福州-> 郑州-> 兰州
"""
def lest_city_passed_by(path):
    return len(path)

def shortest_path(path):
    distance = 0
    for i in range(len(path)-1):
        distance += get_geo_distance(path[i], path[i+1])
    return distance


# 下面在多条路径中通过不同策略进行推荐
def search(begin, end, sort_candidate):
    return sorted(bfs_search(begin, end), key=sort_candidate)[0]

#分别通过最少站数和最短路程查询的路径
print(search('沈阳', '长沙', shortest_path))
print(search('沈阳', '长沙', lest_city_passed_by))
