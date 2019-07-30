# coding=utf-8
# 可视化地铁图及完成路径搜索
import networkx as nx
import matplotlib.pyplot as plt
import math

subway_sites_file = open("./subway_sites.txt", "r", encoding="utf8")
sites_coordinate_file = open("./sites_coordinate.txt", "r", encoding="utf8")

sites_connection = {}
sites_coordinate = {}
sites_subway = {}

# 读取站点坐标
last_site = None
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
    # print(sites[0])
    for i in range(1, len(sites)):
        if sites[i] not in sites_subway:
            sites_subway[sites[i]] = []
        sites_subway[sites[i]].append(sites[0])
        if sites[i] not in sites_connection:
            sites_connection[sites[i]] = set()
        if i > 1:
            sites_connection[sites[i]].add(sites[i-1])
        if i < len(sites)-1:
            sites_connection[sites[i]].add(sites[i+1])
    # sites_gragh = nx.MultiGraph(sites_connection)
    # nx.draw(sites_gragh, sites_coordinate, with_labels=True, node_size=12, font_family='YouYuan', font_size=7)
    # plt.show()

subway_sites_file.close()
sites_coordinate_file.close()

sites_gragh = nx.MultiGraph(sites_connection)
nx.draw(sites_gragh, sites_coordinate, with_labels=True, node_size=12, font_family='YouYuan', font_size=8)
plt.show()


# 还是很丑,因该是nx对应方法和参数问题,回头再研究,先写搜索方法

def bfs_search(begin, end):
    pathes = [[begin]]
    result = []
    if begin not in sites_connection:
        return []
    if end not in sites_connection:
        return []
    while pathes:
        path = pathes.pop(0)
        if path[-1] not in sites_connection:
            continue
        next_sites = sites_connection[path[-1]]
        for site in next_sites:
            if site not in sites_connection:
                continue
            if site in path:
                continue
            if site == end:
                path.append(site)
                result.append(path)
                print(path)
                continue
            new_path = path + [site]
            pathes.append(new_path)
    return result


# 直接搜索不加策略，如果是中间涉及换成，结果会很久很久出不来，但是大多数是没有意义的(绕路了)，需要加策略
# print(bfs_search('北安河站', '焦化厂站'))


# 根据经纬度计算距离
def geo_distance(origin, destination):
    if origin not in sites_coordinate or destination not in sites_coordinate:
        raise Exception('不能识别的站点')
    long1, lat1 = sites_coordinate[origin]
    long2, lat2 = sites_coordinate[destination]
    radius = 6371
    # 两地间弧度计算，经纬度也就是角度值
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(long2 - long1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius * c

# 求数组交集，用来判断几个换乘站点是否在同一线路上
def SINTER(a, b):
    import collections
    A, B = map(collections.Counter, (a, b))
    # collections.Counter & 求两个collections.Counter中相同元素的最小频次
    return list((A&B).elements())


# 判断是否换乘(需要往前两站来判断)
def judge_transfered(cur, prior, pp):
    a = SINTER(sites_subway[cur], sites_subway[prior])
    b = SINTER(sites_subway[prior], sites_subway[pp])
    if SINTER(a, b):
        return False
    else:
        return True


# 路程最短或者最少换成或者综合(换乘一次相当于路程增加5km)
def policy_search(begin, end, policy='shortest'):
    if policy not in ['shortest', 'least', 'comprehensive']:
        raise NameError("Undefined policy.")
    # 这里会定义一个权值 v = k1*距离 + k2*换乘次数
    # 根据策略不同，k1 和 k2 的权值不同
    # 搜索过程中超过当前最小值的会被终止
    distance_k = 0
    freq_k = 0
    if policy == 'shortest':
        distance_k = 1
    if policy == 'least':
        freq_k = 1
    if policy == 'comprehensive':
        distance_k = 1
        freq_k = 5
    min_value = float('inf')
    pathes = [[begin]]
    pathes_value = [0]
    result = []
    if begin not in sites_connection:
        return []
    if end not in sites_connection:
        return []
    while pathes:
        path = pathes.pop(0)
        path_value = pathes_value.pop(0)
        if path[-1] not in sites_connection:
            continue
        next_sites = sites_connection[path[-1]]
        for site in next_sites:
            if site not in sites_connection:
                continue
            if site in path:
                continue
            if path_value > min_value:
                continue
            if site == end:
                path.append(site)
                result = path
                min_value = path_value
                continue
            new_path = path + [site]
            pathes.append(new_path)
            # 地理距离
            path_value = path_value + distance_k * geo_distance(new_path[-1], new_path[-2])
            # 是否换乘了
            if len(path)>2:
                if judge_transfered(path[-3], path[-2], path[-1]):
                    path_value = path_value + freq_k
            pathes_value.append(path_value)
    return result


print("->".join(policy_search('北安河站', '焦化厂站', 'least')))
print("->".join(policy_search('北安河站', '焦化厂站', 'shortest')))
print("->".join(policy_search('北安河站', '焦化厂站', 'comprehensive')))