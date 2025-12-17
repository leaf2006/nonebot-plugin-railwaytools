# Copyright © Leaf developer 2023-2026
# 本文件负责实现“列车查询”功能，部分灵感来源于GitHub项目https://github.com/zmy15/ChinaRailway，特此注明

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

train_info = on_command("列车查询",aliases={"cx","查询"},priority=5,block=True)
def time_Formatter_1(time) -> str: # 格式化时间，1145 -> 11:45
    return time[:2] + ":" + time[2:]

def EMU_code_formatter(str): # 格式化动车组车号 CRH2A2001 -> CRH2A-2001
    return str[:-4] + "-" + str[-4:]
@train_info.handle() # 通过车次查询列车具体信息，不只是能查询动车组，普速列车也可查询
async def handle_train_info(args: Message = CommandArg()): # type: ignore
    if train_Number_in_Info := args.extract_plain_text():
        async with httpx.AsyncClient() as client:

            toDay = datetime.date.today().strftime("%Y%m%d") #获取今日时间，以%Y%m%d的格式形式输出
            
            info_data = {
                "trainCode" : train_Number_in_Info.upper(),
                "startDay" : toDay
            }

            info_res = await client.post(API.api_12306,data=info_data)
            info_Back_data = json.loads(info_res.text) # 对返回数据进行处理

            # 对返回数据进行分析
            stop_time = info_Back_data['data']['trainDetail']['stopTime']

            start_Station_name = stop_time[0]['start_station_name'] # 始发站名
            end_Station_name = stop_time[0]['end_station_name'] # 终到站名

            jiaolu_Corporation_code = stop_time[0]["jiaolu_corporation_code"] # 担当客运段
            if info_data["trainCode"][0] == "D" or info_data["trainCode"][0] == "G" or info_data["trainCode"][0] == "C":
                link_emu_number = API.api_rail_re + "train/" + info_data["trainCode"]
                res_info_EMU = await client.get(link_emu_number)
                info_EMU_code = json.loads(res_info_EMU.text)
                jiaolu_Train_style = EMU_code_formatter(info_EMU_code[0]['emu_no'])

            else:
                jiaolu_Train_style = stop_time[0]["jiaolu_train_style"] # 车底类型
            jiaolu_Dept_train = stop_time[0]["jiaolu_dept_train"] # 车底配属

            stop_inf = []
            stop_dict = {}

            for stop in stop_time: # 遍历该列车的所有站点、到点、发点、停车时间
                station = stop['stationName']
                arrive_time = time_Formatter_1(stop['arriveTime'])
                start_time = time_Formatter_1(stop['startTime'])
                stopover_time = stop['stopover_time'] + "分"
                stop_dict.setdefault("站点",station)
                stop_dict.setdefault("到点",arrive_time)
                stop_dict.setdefault("发点",start_time)
                stop_dict.setdefault("停车时间",stopover_time)
                stop_inf.append(stop_dict)
                stop_dict = {}

            station_result = ""
            station_result_number = 1 # 给时刻表标上序号
            for stop in stop_inf: # 想办法整出时刻表的结果，最后将结果添加到Message中去
                station_result += str(station_result_number) + "." + stop['站点'] + "：" + stop['到点'] + "到," + stop['发点'] + "开，停车" + stop['停车时间'] + "\n"
                station_result_number += 1

            train_info_result = Message([ #结果Message
                "车次：",train_Number_in_Info.upper(),
                "（",start_Station_name , "——" , end_Station_name , ") \n",
                "担当客运段：" , jiaolu_Corporation_code , "\n",
                "车型信息：" , jiaolu_Train_style , "\n",
                "配属：" , jiaolu_Dept_train , "\n \n",
                "----------停站信息----------\n",
                station_result,
                "------------------------------",
            ]) # type: ignore

            await train_info.finish(train_info_result)

    else:
        await train_info.finish("请输入正确的列车车次！（如：Z99）")

