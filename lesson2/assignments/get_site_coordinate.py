# coding=utf-8
# 从百度地图获取站点经纬度信息
import requests
from urllib import parse
import hashlib
import time

# bdmap_map_ak = "3FkAjGKfe0h4gfDFbiFAqW7eyDGO9Fpf"
# bdmap_map_sk = "o24gXmxCcodxHEmXoFfKDzLB2Rc8QMB4"

gaode_key = "fc47596d00144bb87f35de3ea2bf0fd4"
# 根据高德地图地图编码得到访问URL
def get_url(address, city):
    # queryStr = "/geocoding/v3/?address=%s&output=json&ak=%s&city=%s"%(address, bdmap_map_ak, city)
    # # 保留字编码
    # encodeStr = parse.quote(queryStr, safe="!*'();:@&=+$,/?%#[]")
    # rawStr = encodeStr + bdmap_map_sk
    # sn = hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest()
    # url = parse.quote("http://api.map.baidu.com"+queryStr+"&sn="+sn, safe="!*'();:@&=+$,/?%#[]")
    # params = "address=%s&city=%s&output=JSON&key=%s"%(address, city, gaode_key)
    # params = "&".join(params.split("&"))
    # sig = hashlib.md5(params.encode("utf8")).hexdigest()
    # queryUrl = "https://restapi.amap.com/v3/geocode/geo?%s&sig=%s"%(params, sig)

    ##API都不准，从高德工具爬了一个
    time.sleep(0.1)
    queryUrl = "https://restapi.amap.com/v3/place/text?s=rsv3&children=&key=8325164e247e15eea68b59e89200988b&page=1&offset=10&city=440300&language=zh_cn&platform=JS&logversion=2.0&sdkversion=1.3&appname=https%3A%2F%2Flbs.amap.com%2Fconsole%2Fshow%2Fpicker&csid=2BA8231C-F0F5-49F5-87A0-F0C388CDF89F&keywords="+address
    return queryUrl


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
    line_content = line.replace('\n', '').split(",")
    line_name = line_content[0]
    for site_name in line_content[1:]:
        if site_name in sites_seen:
            continue
        sites_seen.add(site_name)
        result = get_site_coordinate("北京市"+site_name, "北京市")
        if result['status'] == '1' and int(result['count']) > 0:
            lng, lat = result['pois'][0]['location'].split(",")
            print(site_name, lng, lat)
            sites_coordinate_file.write("%s,%s,%s\n"%(site_name, lng, lat))
        else:
            sites_coordinate_file.write("%s,%f,%f\n" % (site_name, 0, 0))
            print(site_name, result)

sites_coordinate_file.close()
sites_coordinate_file.close()

