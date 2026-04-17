# Copyright © Leaf developer 2023-2026
# 本文件负责实现“查询线路信息”功能

import httpx
import json
from nonebot import on_command   # type: ignore
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment   # type: ignore
from nonebot.plugin import PluginMetadata  # type: ignore
from nonebot.params import CommandArg  # type: ignore
from nonebot.rule import to_me  # type: ignore
from .utils import utils
from .api import API

route_info = on_command("线路",aliases={"xl","线路信息","线","铁路"},priority=5,block=True)

@route_info.handle()
async def handle_route_info(event:Event, args: Message = CommandArg()):
    raw_message = str(event.get_message()).strip()
    command_part = utils.get_command_part(raw_message)
    valid_commands = ['线路','xl','线路信息','线','铁路']
    if command_part not in valid_commands:
        return
        
    if route_name_input := args.extract_plain_text():

        is_hsr = False
        if "铁路" in route_name_input: # 防止搜索出现错误
            route_name_input = route_name_input.replace("铁路","")
            # is_hsr = False
        elif "线" in route_name_input:
            route_name_input = route_name_input.replace("线","")
            # is_hsr = False
        elif "高铁" in route_name_input:
            route_name_input = route_name_input.replace("高铁","")
            is_hsr = True # 判定是否为高速铁路
        else:
            pass
        
        try:
            async with httpx.AsyncClient(headers=API.headers) as client:
                res_search_data = await utils.cnrail_search(route_name_input)
                if not res_search_data:
                    await route_info.finish("未收录该线路或线路不存在，请重新输入！")
                else:
                    for i in range(len(res_search_data)): # 搜索在所有搜索结果中属于“铁路”类别的条目
                        search_query = res_search_data[i]['query']
                        search_name = res_search_data[i]['name']
                        if "rail/" in search_query:
                            if is_hsr == False:
                                if "高速" not in search_name:
                                    break
                            else:
                                break

                    rail_id = search_query.replace("rail/","") # 去除query中的前缀rail/，这部分将不作为rail_id使用
                
                url_route_info = f"{API.api_cnrail_geogv}feature/{rail_id}?locale=zhcn" # 已更新为新版调用方式
                route_info_res = await client.get(url_route_info)
                route_info_raw_data = json.loads(route_info_res.text)
                route_info_data = route_info_raw_data['data']

                route_info_name = route_info_data['name'] # 线路名称

                if route_info_data['lines'] == "2": # 线路形态
                    route_info_linenum = "复线铁路"
                elif route_info_data['lines'] == "1":
                    route_info_linenum = "单线铁路"
                else:
                    route_info_linenum = route_info_data['lines']
                
                design_speed_raw = route_info_data.get("design_speed")
                if not design_speed_raw or str(design_speed_raw).strip().lower() == "null":
                    route_info_designSpeed = "暂无数据"
                else:
                    route_info_designSpeed = str(design_speed_raw)

                route_info_railType = route_info_data['railtype'] # 新版模式
                
                # 作者心还怪好的，新版调用方式的那个stations确实比原来的好
                stations_list = route_info_data['stations']
                if not stations_list or stations_list == "null":
                    route_info_stations = "暂无沿途车站数据"
                else:
                    route_info_stations = ""
                    for counts in range(len(stations_list)):
                        station_name = stations_list[counts]['name']
                        kilometerage_raw = stations_list[counts]['mileage']
                        if kilometerage_raw is None:
                            kilometerage = ""
                        else:
                            kilometerage = f"{kilometerage_raw}Km"
                        route_info_stations += f"【{str(counts+1)}】{station_name}         {kilometerage} \n"

                # 这里跟随原网站弃用“服务类型”
                route_info_result = Message([
                    "【",route_info_name,"】线路信息：\n"
                    "线路类型：",route_info_railType,"\n",
                    "单/复线：",route_info_linenum,"\n",
                    "设计时速：",route_info_designSpeed,"\n \n",
                    "----------沿途车站----------\n",
                    route_info_stations,
                    "------------------------------ \n \n",
                    "*本表所列起点终点为该线路里程接算站，里程为营业用运价里程，与线路实际运行长度并不相同\n"
                    "数据来源：cnrail.geogv.org",
                ])

        except (httpx.ReadTimeout,httpx.ConnectTimeout):
            route_info_result = "请求超时，请稍等一下再试"
        except Exception as error:
            route_info_result = "发生异常：" + str(error)

        await route_info.finish(route_info_result)

    else:
        await route_info.finish("请输入线路名称")
