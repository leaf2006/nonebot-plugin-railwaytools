# Copyright © Leaf developer 2023-2026
# 本文件负责实现“车站大屏”功能，使用第三方API，仅供参考，请勿用于实际乘车

import json
import datetime  
import httpx
from nonebot import on_command   # type: ignore
from nonebot.adapters.onebot.v11 import Message, MessageSegment   # type: ignore
from nonebot.plugin import PluginMetadata  # type: ignore
from .config import Config
from nonebot.params import CommandArg  # type: ignore
from nonebot.rule import to_me  # type: ignore
from .api import API  

station_screen = on_command("大屏",aliases={"dp","车站大屏"},priority=5,block=True)
def time_Formatter_2(time) -> str: # 格式化时间，2025-12-17 14:50:00 -> 14:50
    return time[11:16]

@station_screen.handle()
async def handle_station_screen(args: Message = CommandArg()):
    if station_Name_input := args.extract_plain_text():
        async with httpx.AsyncClient() as client:
            link_Station_screen = API.api_station_screen + station_Name_input
            res_Train_list = await client.get(link_Station_screen)
            res_data = json.loads(res_Train_list.text)
            identification_code = str(res_data['code']) # API返回的识别码

            # 识别码200：有数据；识别码404：无数据

            if identification_code == "200":
                data_list = res_data['data']['data']
                fetch_time = res_data['data']['fetch_time']
                num = len(data_list)
                count = 1 # 在每个列车信息前标数
                result = ""
                for i in range(num):
                    if i <= 9:
                        train_code = data_list[i][0]
                        start_Station_name = data_list[i][1]
                        end_Station_name = data_list[i][2]
                        departure_time = time_Formatter_2(data_list[i][3])
                        status = data_list[i][5]
                        result += f"【{count}】{train_code}（{start_Station_name}——{end_Station_name}）{departure_time}开 ， 状态：{status} \n"
                        count += 1

                    else:
                        pass
                
                result_message = Message([
                    f"【{station_Name_input}站】车站大屏如下：\n \n",
                    "------------------------------ \n",
                    result,
                    "------------------------------ \n \n",
                    "仅显示该车站部分列车信息。本车站大屏来源于第三方API，及供参考，请勿用于实际乘车！\n",
                    f"数据刷新时间：{fetch_time}",
                ])

                await station_screen.finish(result_message)

            else:
                await station_screen.finish("您输入的车站名不存在或未收录，请重新输入！")
                
    
    else:
        await station_screen.finish("请输入正确的车站名！（如：上海）")

