# Copyright © Leaf developer 2023-2026
# 本文件负责实现“查询车站信息”功能

import httpx
import json 
from nonebot import on_command 
from nonebot.adapters.onebot.v11 import Message, MessageSegment 
from nonebot.plugin import PluginMetadata
from nonebot.params import CommandArg 
from nonebot.rule import to_me
from .utils import utils 
from .api import API

station_info = on_command("车站",aliases={"cz","车站信息","站"},priority=5,block=True)

@station_info.handle()
async def handle_station_info(args: Message = CommandArg()):
    if station_name_input := args.extract_plain_text():
        if "站" in station_name_input: # 防止搜索出现问题
            station_name_input = station_name_input.replace("站","")
        elif "车站" in station_name_input:
            station_name_input = station_name_input("车站","")
        else:
            pass

        try:
            async with httpx.AsyncClient(headers=API.headers) as client:
                res_search_data = await utils.cnrail_search(station_name_input)
                if not res_search_data:
                    await station_info.finish("未收录该车站或车站不存在，请重新输入！")
                else:
                    for i in range(len(res_search_data)): # 搜索所有搜索结果中属于“车站”类别的 条目
                        if res_search_data[i][2] == station_name_input and res_search_data[i][1] == "STATION":
                            continue_search = False
                            break
                        else:
                            continue_search = True
                    
                    if continue_search == True:
                        for i in range(len(res_search_data)):
                            if res_search_data[i][1] == "STATION":
                                break
                    else:
                        pass        

                    rail_id = res_search_data[i][0]

                url_sta_basic_info = f"{API.api_cnrail_geogv}station/{rail_id}?locale=zhcn&query-override=&requestGeom=true" # 车站基本信息
                url_sta_route_info = f"{API.api_cnrail_geogv}station-link/{rail_id}?locale=zhcn&query-override=" # 车站所属线路
                
                sta_basic_info_res = await client.get(url_sta_basic_info)
                sta_basic_info_data = json.loads(sta_basic_info_res.text) # 返回数据直接可以使用，没有套了个"data":{}的壳
                
                sta_route_info_res = await client.get(url_sta_route_info)
                sta_route_info_rawdata = json.loads(sta_route_info_res.text)

                sta_telecode_rawdata = sta_basic_info_data['teleCode'] # 电报码
                sta_pinyincode_rawdata = sta_basic_info_data['pinyinCode'] # 拼音码
                sta_location_rawdata = sta_basic_info_data['location'] # 所在地点
                sta_serviceclass_rawdata = sta_basic_info_data['serviceClass'] # 服务类型

                sta_name = sta_basic_info_data['localName'] # 车站名称
                sta_bureau = "所属路局：" + sta_basic_info_data['bureau'].get("name") + "\n" # 所属单位
                
                if not sta_telecode_rawdata or sta_telecode_rawdata.strip() == "null":
                    sta_telecode = ""
                else:
                    sta_telecode = f"电报码：{sta_telecode_rawdata}\n"

                if not sta_pinyincode_rawdata or sta_pinyincode_rawdata.strip() == "null":
                    sta_pinyincode = ""
                else:
                    sta_pinyincode = f"拼音码：{sta_pinyincode_rawdata}\n"

                if not sta_location_rawdata or sta_location_rawdata.strip() == "null":
                    sta_location = ""
                else:
                    sta_location = f"位置：{sta_location_rawdata}\n" 

                if sta_serviceclass_rawdata == "":
                    sta_serviceclass = "本站不办理客运业务\n"
                else:
                    sta_serviceclass = "本站办理客运业务\n"

                hr_line = "------------------------------ \n"
                if sta_route_info_rawdata['success'] == False:
                    sta_route_info_result = f"{hr_line}暂无该车站线路数据\n"
                else:
                    sta_route_info_data = sta_route_info_rawdata['data']
                    sta_route_info_result = ""
                    for i in range(len(sta_route_info_data)):
                        railname = sta_route_info_data[i]['railName']

                        next_station_raw = sta_route_info_data[i]['next'][0][2]
                        terminal_station_raw = sta_route_info_data[i]['next'][0][8]
                        if next_station_raw == "*" and terminal_station_raw == "*":
                            next_station = "起迄站"
                            terminal_station = ""
                        else:
                            next_station = next_station_raw
                            terminal_station = f"（{terminal_station_raw}）方向"

                        prev_station_raw = sta_route_info_data[i]['prev'][0][2]
                        starting_station_raw = sta_route_info_data[i]['prev'][0][8]
                        if prev_station_raw == "*" and starting_station_raw == "*":
                            prev_station = "起迄站"
                            starting_station = ""
                        else:
                            prev_station = prev_station_raw
                            starting_station = f"（{starting_station_raw}）方向"

                        sta_route_info_result += f"{hr_line}【{railname}】\n 下站{terminal_station}：{next_station}\n 上站{starting_station}：{prev_station}\n"


                sta_info_result = Message([
                    "【",sta_name,"】基础信息如下：\n",
                    sta_telecode,
                    sta_pinyincode,
                    sta_bureau,
                    sta_location,
                    sta_serviceclass,
                    sta_route_info_result,
                    "------------------------------\n \n",
                    "数据来源：cnrail.geogv.org",

                ])
        except (httpx.ReadTimeout,httpx.ConnectTimeout):
            sta_info_result = "请求超时，请稍等一下再试"
        except Exception as error:
            route_info_result = "发生异常：" + str(error)
            
        await station_info.finish(sta_info_result)

    else:
        await station_info.finish("请输入线路名称")
        
