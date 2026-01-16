# Copyright © Leaf developer 2023-2026
# 本文件负责实现“车站大屏”功能，使用第三方API，仅供参考，请勿用于实际乘车

import json
import datetime  
import httpx
from nonebot import on_command   # type: ignore
from nonebot.adapters.onebot.v11 import Message, MessageSegment   # type: ignore
from nonebot.plugin import PluginMetadata  # type: ignore
from nonebot.params import CommandArg  # type: ignore
from nonebot.rule import to_me  # type: ignore
from .utils import utils
from .api import API  

station_screen = on_command("大屏",aliases={"dp","车站大屏"},priority=5,block=True)
# def time_Formatter_2(time) -> str: # 格式化时间，2025-12-17 14:50:00 -> 14:50
#     return time[11:16]

@station_screen.handle()
async def handle_station_screen(args: Message = CommandArg()):
    if station_name_input := args.extract_plain_text():

        if "站" in station_name_input:
            station_name_input = station_name_input.replace("站","")
        elif "车站" in station_name_input:
            station_name_input = station_name_input.replace("车站","")
        else:
            pass

        async with httpx.AsyncClient(headers=API.headers) as client:
            url_station_screen = f"{API.api_station_screen}msg={station_name_input}&type=json&page=1"
            res_train_list = await client.get(url_station_screen)
            res_data = json.loads(res_train_list.text)

            if "error" in res_data:
                await station_screen.finish("您输入的车站名不存在或未收录，请重新输入！")
            
            else:
                data_list = res_data['当前页车次列表']
                count = 1 # 在每个列车信息前标数
                result = ""
                hr_line = "------------------------------ \n"
                for i in range(len(data_list)):
                    if i <= 9:
                        train_code = data_list[i]['车次号']
                        start_station_name = data_list[i]['出发地']
                        end_station_name = data_list[i]['目的地']
                        departure_time = utils.time_Formatter_2(data_list[i]['出发时间'])
                        waitingroom_and_check_in = data_list[i]['候车室/检票口']
                        status = data_list[i]['状态']
                        result += f"{hr_line}【{count}】{train_code}（{start_station_name}——{end_station_name}）\n发车时间：{departure_time}\n候车室/检票口：{waitingroom_and_check_in}\n状态：{status}\n"
                        count += 1

                    else:
                        pass
                station_screen_message = Message([
                    f"【{station_name_input}站】车站大屏如下：\n \n",
                    result,
                    hr_line,"\n",
                    "仅显示该车站部分列车信息。本车站大屏来源于第三方API，及供参考，请勿用于实际乘车！\n",
                ])
                await station_screen.finish(station_screen_message)
                
    else:
        await station_screen.finish("请输入正确的车站名！（如：上海）")