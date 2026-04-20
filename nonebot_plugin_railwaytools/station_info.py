# Copyright © Leaf developer 2023-2026
# 本文件负责实现“查询车站信息”功能

import httpx
import json 
from nonebot import on_command
from nonebot.adapters import Event 
from nonebot.adapters.onebot.v11 import Message, MessageSegment 
from nonebot.plugin import PluginMetadata
from nonebot.params import CommandArg 
from nonebot.rule import to_me
from .utils import utils 
from .api import API

station_info = on_command("车站",aliases={"cz","车站信息","站"},priority=5,block=True)

@station_info.handle()
async def handle_station_info(event:Event, args: Message = CommandArg()):
    raw_message = str(event.get_message()).strip()
    command_part = utils.get_command_part(raw_message)
    valid_commands = ['车站','cz','车站信息','站']
    if command_part not in valid_commands:
        return    
    if station_name_input := args.extract_plain_text():
        is_metro_sta = False
        if "地铁站" in station_name_input:
            station_name_input = station_name_input.replace("地铁站","")
            is_metro_sta = True
        elif "站" in station_name_input: # 防止搜索出现问题
            station_name_input = station_name_input.replace("站","")
        elif "车站" in station_name_input:
            station_name_input = station_name_input.replace("车站","")
        else:
            pass

        try:
            async with httpx.AsyncClient(headers=API.headers) as client:
                res_search_data = await utils.cnrail_search(station_name_input)
                if not res_search_data:
                    await station_info.finish("未收录该车站或车站不存在，请重新输入！")
                else:
                    # 为了适应网站加入了地铁的新特性，将搜索与获取数据两步放在一起，便于对地铁车站与国铁车站重名现象的处理
                    sta_info_formatted_data = ""
                    for search_results in res_search_data:
                        search_query = search_results['query']
                        search_name = search_results['name']
                        if "geo/" in search_query and station_name_input == search_name:
                            sta_id = search_query.replace("geo/","")
                            url_sta_info = f"{API.api_cnrail_geogv}poi/{sta_id}?locale=zhcn"
                            sta_info_res = await client.get(url_sta_info)
                            sta_info_formatted_data = utils.decrypt_cnrail_data(sta_info_res.text)

                            if is_metro_sta == True:
                                if sta_info_formatted_data['featureType'] == "地铁站":
                                    break
                            else:
                                if sta_info_formatted_data['featureType'] == "火车站":
                                    break

                sta_status_judge = sta_info_formatted_data['featureType'] # 上一步判断车站类型是为了筛选重名地铁站，防止误选，这里不是
                if sta_status_judge == "地铁站":
                    is_metro_sta = True

                sta_detail = sta_info_formatted_data['exd'][0]['data']
                # 站名
                if is_metro_sta == True:
                    sta_name = sta_info_formatted_data['name'] + "地铁站"
                else:
                    sta_name = sta_info_formatted_data['name']
                
                # 电报码
                sta_telecode_raw = sta_detail.get("tele_code")
                if not sta_telecode_raw or str(sta_telecode_raw).strip() == "null":
                    sta_telecode = ""
                else:
                    sta_telecode = f"电报码：{sta_detail['tele_code']}\n"
                
                sta_bureau = f"所属单位：{sta_detail['operators'][0]['name']}\n"
                sta_location = f"位置：{sta_info_formatted_data['location']}\n"

                serviceclass_judge = sta_detail.get('trainservice')
                if is_metro_sta == True:
                    sta_serviceclass = "" # 地铁车站特殊处理                
                elif not serviceclass_judge and is_metro_sta == False:
                    sta_serviceclass = "本站不办理客运业务\n"
                else:
                    sta_serviceclass = "本站办理客运业务\n"
                
                hr_line = "------------------------------ \n"
                # 沿途车站
                
                if not sta_detail.get('connection'):
                    sta_route_info = f"{hr_line}暂无该车站线路数据\n"
                else:
                    sta_route_data = sta_detail['connection']
                    sta_route_info = ""
                    for route in sta_route_data:
                        linename = route['linename']
                        next_data = route['next'][0]
                        if next_data.get('adj'): # 如果下一站不是null，则必然有dest_station；如果下一站是null，本站必然是终点站
                            next_sta = next_data['adj']['name']
                            next_dest_sta = f"（{next_data['dest']['name']}）方向"
                        else:
                            if next_data['dest']['status'] == "END":
                                next_sta = "起迄站"
                                next_dest_sta = ""

                        prev_data = route['prev'][0]
                        if prev_data.get('adj'):
                            prev_sta = prev_data['adj']['name']
                            prev_dest_sta = f"（{prev_data['dest']['name']}）方向"
                        else:
                            if prev_data['dest']['status'] == "END":
                                prev_sta = "起迄站"
                                prev_dest_sta = ""
                    
                        sta_route_info += f"{hr_line}【{linename}】\n下站{next_dest_sta}：{next_sta}\n上站{prev_dest_sta}：{prev_sta}\n"
                         # TODO

                sta_info_result = Message([
                    "【",sta_name,"】基础信息如下：\n",
                    sta_telecode,
                    sta_bureau,
                    sta_location,
                    sta_serviceclass,
                    sta_route_info,
                    "------------------------------\n \n",
                    "数据来源：cnrail.geogv.org",

                ])
        except (httpx.ReadTimeout,httpx.ConnectTimeout):
            sta_info_result = "请求超时，请稍等一下再试"
        except Exception as error:
            sta_info_result = "发生异常：" + str(error)
            
        await station_info.finish(sta_info_result)

    else:
        await station_info.finish("请输入线路名称")
        
