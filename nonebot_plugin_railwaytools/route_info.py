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
                        if res_search_data[i][1] == "RAIL":
                            if is_hsr == False:
                                if "高速" not in res_search_data[i][2]:
                                    break
                            else:
                                break

                    rail_id = res_search_data[i][0]
                
                # print(rail_id)
                url_route_info = f"{API.api_cnrail_geogv}rail/{rail_id}?locale=zhcn"
                route_info_res = await client.get(url_route_info)
                route_info_raw_data = json.loads(route_info_res.text)
                route_info_data = route_info_raw_data['data']

                route_info_name = route_info_data['name'] # 线路名称

                if route_info_data['lineNum'] == "2": # 线路形态
                    route_info_linenum = "复线铁路"
                elif route_info_data['lineNum'] == "1":
                    route_info_linenum = "单线铁路"
                else:
                    route_info_linenum = route_info_data['lineNum']
                
                if not route_info_data['designSpeed'] or route_info_data['designSpeed'].strip() == "null": # 设计时速
                    route_info_designSpeed = "暂无数据"
                else:
                    route_info_designSpeed = route_info_data['designSpeed']

                if route_info_data['railService'] == "F": # 服务类型
                    route_info_railService = "货运"
                elif route_info_data['railService'] == "P":
                    route_info_railService = "客运"
                elif route_info_data['railService'] == "PF":
                    route_info_railService = "客货两用"
                elif route_info_data['railService'] == "P2F1":
                    route_info_railService = "客运为主，兼顾货运"
                else:
                    route_info_railService = route_info_data['railService']
                
                if route_info_data['railType'] == "CONV": # 线路类型
                    route_info_railType = "普速铁路"
                elif route_info_data['railType'] == "RR":
                    route_info_railType = "快速铁路"
                elif route_info_data['railType'] == "HSR":
                    route_info_railType = "高速铁路"
                else:
                    route_info_railType = route_info_data['railType']
                
                if route_info_data['diagram'] == "null":
                    route_info_diagram = "暂无沿途车站数据"
                else:
                    raw_diagram = route_info_data['diagram']['records']
                    # route_info_diagram = raw_diagram[num][3][0][2]
                    route_info_diagram = ""
                    num = 0
                    count = 1
                    count_raw_diagram = len(raw_diagram) - 1
                    while num < count_raw_diagram:
                        if not raw_diagram[num][3] or raw_diagram[num][2] not in ['SST','MST']:
                            num += 1
                            continue

                        station_name = raw_diagram[num][3][0][2]
                        raw_kilometerage = str(raw_diagram[num][1])
                        if raw_kilometerage.strip() == "":
                            kilometerage = ""
                        else:
                            kilometerage = f"{raw_kilometerage}Km"
                        route_info_diagram += f"【{str(count)}】{station_name}         {kilometerage} \n"
                        count += 1
                        num += 1


                route_info_result = Message([
                    # "线路名称：",route_info_name,"\n",
                    "【",route_info_name,"】线路信息：\n"
                    "线路类型：",route_info_railType,"\n",
                    "服务类型：",route_info_railService,"\n",
                    "单/复线：",route_info_linenum,"\n",
                    "设计时速：",route_info_designSpeed,"\n \n",
                    "----------沿途车站----------\n",
                    route_info_diagram,
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
