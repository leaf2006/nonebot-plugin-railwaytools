# Copyright © Leaf developer 2023-2025
# 代码写的一坨屎，一堆功能挤在__init__.py，轻点喷qwq
# 本项目中“列车查询”的部分功能灵感来源于GitHub项目https://github.com/zmy15/ChinaRailway，特此注明

import json
import requests
import datetime  
from nonebot import on_command  
from nonebot.adapters.onebot.v11 import Message, MessageSegment  
from nonebot.params import CommandArg  
from nonebot.rule import to_me
from .api import API  

emu_number = on_command("车号",aliases={"ch", "查车号"}, priority=5,block=True)
train_number = on_command("车次",aliases={"cc", "查车次"}, priority=5,block=True)
xiaguanzhan_photo = on_command("下关站",aliases={"xgz"},priority=5,block=True)
train_info = on_command("列车查询",aliases={"cx","查询"},priority=5,block=True)
information_helper = on_command("help",aliases={"帮助"},priority=6,block=True)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}  # noqa: E501

@emu_number.handle() #通过车次查询车组号
async def handle_function(args: Message = CommandArg()): # type: ignore
    if number := args.extract_plain_text():  # noqa: F841
        link_emu_number = API.api_rail_re + 'train/' + number.upper()
        x = requests.get(link_emu_number, headers=headers)
        data = json.loads(x.text)
        num = 0
        final_result = ""
        while num < 8:
            result = data[num]['emu_no']
            time = data[num]['date']
            final_result += time + '：' +result + "\n"
            num += 1
            print_out = number.upper() + '次列车近8次担当的车组号为：\n' + final_result
        await emu_number.finish(print_out) # type: ignore

    else:
        await emu_number.finish("请输入车号")


@train_number.handle() #通过车组号查询车次
async def handle_function(args: Message = CommandArg()): # type: ignore
    if number := args.extract_plain_text():  # noqa: F841
        link_train_number = API.api_rail_re + 'emu/' + number.upper()
        x = requests.get(link_train_number, headers=headers)
        data = json.loads(x.text)
        num = 0
        final_result = ""
        while num < 8:
            result = data[num]['train_no']
            time = data[num]['date']
            final_result += time + '：' +result + "\n"
            num += 1
            print_out = number.upper() + '近8次担当的车次为：\n' + final_result
        await train_number.finish(print_out) # type: ignore

    else:
        await train_number.finish("请输入车次")

@xiaguanzhan_photo.handle() #查询下关站列车户口照
async def handle_function(args: Message = CommandArg()): # type: ignore
    if number := args.extract_plain_text():
        await xiaguanzhan_photo.send("正在加载图片，时间可能略久...")
        photo = API.api_xiaguanzhan + number + ".jpg"
        await xiaguanzhan_photo.finish(MessageSegment.image(photo))
    else:
        await xiaguanzhan_photo.finish("请输入正确的车号!，如：DF7C-5030")

@train_info.handle() # 通过车次查询列车具体信息，不只是能查询动车组，普速列车也可查询
async def handle_function(args: Message = CommandArg()): # type: ignore
    if train_Number_in_Info := args.extract_plain_text():
        toDay = datetime.date.today().strftime("%Y%m%d") #今日时间，以%Y%m%d的格式形式输出
        
        info_data = {
            "trainCode" : train_Number_in_Info.upper(),
            "startDay" : toDay
        }

        info_res = requests.post(API.api_12306 , data=info_data , headers=headers)
        info_Back_data = json.loads(info_res.text) # 对返回数据进行处理

        # 对返回数据进行分析
        stop_time = info_Back_data['data']['trainDetail']['stopTime']

        start_Station_name = stop_time[0]['start_station_name'] # 始发站名
        end_Station_name = stop_time[0]['end_station_name'] # 终到站名

        jiaolu_Corporation_code = stop_time[0]["jiaolu_corporation_code"] # 担当客运段
        jiaolu_Train_style = stop_time[0]["jiaolu_train_style"] # 车底类型
        jiaolu_Dept_train = stop_time[0]["jiaolu_dept_train"] # 车底配属

        train_info_result = Message([ #结果Message
            "车次：",train_Number_in_Info.upper(),
            "（",start_Station_name , "——" , end_Station_name , ") \n",
            "担当客运段：" , jiaolu_Corporation_code , "\n",
            "车型信息：" , jiaolu_Train_style , "\n",
            "配属：" , jiaolu_Dept_train ,
        ]) # type: ignore

        await train_info.finish(train_info_result)

    else:
        await train_info.finish("请输入正确的列车车次！（如：Z99）")


@information_helper.handle() #帮助页面
async def handle_function():
    information_Helper_message = Message([
        "这是一个火车迷也许觉得很好用的铁路工具箱，具有多种功能 \n \n",
        "----------使用方法----------\n",
        "① 通过车次查询担当的动车组车组号：/车号 或 /ch （例如：/车号 D3211） \n \n",
        "② 通过动车组车组号查询担当车次：/车次 或 /cc （例如：/车次 CRH2A-2001） \n \n",
        "③ 通过车号查询下关站机车户口照：/下关站 或 /xgz （例如：/下关站 DF7C-5030） \n \n",
        "④ 通过列车车次查询该车次的始发终到、担当客运段、车型信息以及配属，同时支持动车组与普速列车：/查询 或 /cx （例如：/查询 Z99）\n \n"
        "⑤ 帮助：/帮助 或 /help \n \n",
        "更多功能正在开发中，尽情期待！ \n",
        "------------------------------ \n \n",
        "Powered by Nonebot2 and Onebot v11\n",
        "Copyright © Leaf developer 2023-2025"

    ]) # type: ignore

    await information_helper.finish(information_Helper_message)