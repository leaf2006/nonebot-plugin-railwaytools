# Copyright © Leaf developer 2023-2026
# 这里存储本插件所需使用的所有API入口与链接

class API:
    api_12306 = "https://mobile.12306.cn/wxxcx/wechat/main/travelServiceQrcodeTrainInfo"
    api_rail_re = "https://api.rail.re/"
    api_EMU_route_schedule = "https://rail.re/img/"
    api_xiaguanzhan = "http://www.xiaguanzhan.com/uploadfiles/"
    api_station_screen = "https://apis.uctb.cn/api/12306?"
    api_cnrail_geogv = "http://cnrail.geogv.org/api/v1/"
    
    headers = { # 加个请求头，保险一点
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }