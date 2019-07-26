# coding=utf-8
# 从百度地图获取站点经纬度信息
import requests
from urllib import parse
import hashlib

bdmap_map_ak = "3FkAjGKfe0h4gfDFbiFAqW7eyDGO9Fpf"
bdmap_map_sk = "o24gXmxCcodxHEmXoFfKDzLB2Rc8QMB4"

# 根据百度地图地图编码API计算sn返回访问URL
def get_url(address, city):
    queryStr = "/geocoding/v3/?address=%s&output=json&ak=%s&city=%s"%(address, bdmap_map_ak, city)
    # 保留字编码
    encodeStr = parse.quote(queryStr, safe="!*'();:@&=+$,/?%#[]")
    rawStr = encodeStr + bdmap_map_sk
    sn = hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest()
    url = parse.quote("http://api.map.baidu.com"+queryStr+"&sn="+sn, safe="!*'();:@&=+$,/?%#[]")
    return url


# 获取对应城市地点的经纬度
def get_site_coordinate(address, city):
    r = requests.get(get_url(address, city))
    return r.json()


# 读取站点并获取其经纬度后保存
sub_sites_file = open("./subway_sites.txt", "r", encoding="utf8")
sites_coordinate_file = open("./sites_coordinate.txt", "w", encoding="utf8")
sites_seen = set()

while True:
    line = sub_sites_file.readline()
    if not line:
        break
    for site_name in line.replace('\n', '').split(",")[1:]:
        if site_name in sites_seen:
            continue
        sites_seen.add(site_name)
        result = get_site_coordinate('北京市'+site_name+'地铁站', "北京市")
        if result['status'] == 0:
            lng, lat = result['result']['location']['lng'], result['result']['location']['lat']
            print(site_name, lng, lat)
            sites_coordinate_file.write("%s,%f,%f\n"%(site_name, lng, lat))
        else:
            sites_coordinate_file.write("%s,%f,%f\n" % (site_name, 0, 0))
            print(site_name, result)

sites_coordinate_file.close()
sites_coordinate_file.close()

