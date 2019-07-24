# coding=utf-8
# 获取站点经纬度信息
import requests
import re
from urllib import parse
import hashlib

bdmap_map_ak = "3FkAjGKfe0h4gfDFbiFAqW7eyDGO9Fpf"
bdmap_map_sk = "o24gXmxCcodxHEmXoFfKDzLB2Rc8QMB4"

def get_url(address, city):
    queryStr = "/geocoding/v3/?address=%s&output=json&ak=%s&city=%s"%(address, bdmap_map_ak, city)
    # 保留字编码
    encodeStr = parse.quote(queryStr, safe="!*'();:@&=+$,/?%#[]")
    rawStr = encodeStr + bdmap_map_sk
    sn = hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest()
    url = parse.quote("http://api.map.baidu.com"+queryStr+"&sn="+sn, safe="!*'();:@&=+$,/?%#[]")
    return url


def get_site_coordinate(address, city):
    r = requests.get(get_url(address, city))
    return r.json()


sites_connection = open("./sites_connection.txt", "r")
sites_coordinate = open("./sites_coordinate.txt", "w")
sites_seen = set()

while True:
    line = sites_connection.readline()
    if not line:
        break
    for site_name in line.replace('\n', '').split(","):
        if site_name in sites_seen:
            continue
        sites_seen.add(site_name)
        result = get_site_coordinate('北京市'+site_name+'地铁站', "北京市")
        if result['status'] == 0:
            lng, lat = result['result']['location']['lng'], result['result']['location']['lat']
            print(site_name, lng, lat)
            sites_coordinate.write("%s,%f,%f\n"%(site_name, lng, lat))
        else:
            sites_coordinate.write("%s,%f,%f\n" % (site_name, 0, 0))
            print(site_name, result)

sites_connection.close()
sites_coordinate.close()

