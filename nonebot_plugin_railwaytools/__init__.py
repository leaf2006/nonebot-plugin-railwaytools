# Copyright © Leaf developer 2023-2025
# 代码写的一坨屎，一堆功能挤在__init__.py，轻点喷qwq
# 本项目少量使用了GitHub Copilot，其中“列车查询”的部分功能灵感来源于GitHub项目https://github.com/zmy15/ChinaRailway，特此注明
import aiohttp
import httpx
import json
import datetime  
from nonebot import on_command   # type: ignore
from nonebot.adapters.onebot.v11 import Message, MessageSegment   # type: ignore
from nonebot.plugin import PluginMetadata  # type: ignore
from .config import Config
from nonebot.params import CommandArg  # type: ignore
from nonebot.rule import to_me  # type: ignore
from .api import API  

# 插件配置页
__plugin_meta__ = PluginMetadata(
    name="火车迷铁路工具箱",
    description="这是一个火车迷也许觉得很好用的铁路机器人工具箱",
    usage="""
    /车号 [动车组车次] - 通过车次查询担当的动车组车组号
    /车次 [动车组车组号] - 通过动车组车组号查询担当车次
    /下关站 [机车车号] - 通过车号查询下关站机车户口照
    /查询 [列车车次] - 通过列车车次查询该车次的始发终到、担当客运段、车型信息、配属以及具体时刻表
    /help - 查看帮助信息
    """,

    type="application",
    # 发布必填，当前有效类型有：`library`（为其他插件编写提供功能），`application`（向机器人用户提供功能）。

    homepage="https://github.com/leaf2006/nonebot-plugin-railwaytools",
    # 发布必填。

    config=Config,
    # 插件配置项类，如无需配置可不填写。

    supported_adapters={"~onebot.v11", "~telegram"},
    # 支持的适配器集合，其中 `~` 在此处代表前缀 `nonebot.adapters.`，其余适配器亦按此格式填写。
    # 若插件可以保证兼容所有适配器（即仅使用基本适配器功能）可不填写，否则应该列出插件支持的适配器。
)

emu_number = on_command("车号",aliases={"ch", "查车号"}, priority=5,block=True)
train_number = on_command("车次",aliases={"cc", "查车次"}, priority=5,block=True)
xiaguanzhan_photo = on_command("下关站",aliases={"xgz"},priority=5,block=True)
train_info = on_command("列车查询",aliases={"cx","查询"},priority=5,block=True)
# station_screen = on_command("大屏",aliases={"dp","车站大屏"},priority=5,block=True)
information_helper = on_command("help",aliases={"帮助"},priority=6,block=True)

def time_Formatter(time) -> str: # 格式化时间，1145 -> 11:45
    return time[:2] + ":" + time[2:]

@emu_number.handle()
async def handle_function(args: Message = CommandArg()): # type: ignore
    if number := args.extract_plain_text():
        async with httpx.AsyncClient() as client:
            link_emu_number = API.api_rail_re + 'train/' + number.upper()
            response = await client.get(link_emu_number)
            data = json.loads(response.text)
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

@xiaguanzhan_photo.handle() #查询下关站列车户口照
async def handle_function(args: Message = CommandArg()): # type: ignore
    if number := args.extract_plain_text():
        await xiaguanzhan_photo.send("正在加载图片，时间可能略久...")
        photo = API.api_xiaguanzhan + number + ".jpg"
        await xiaguanzhan_photo.finish(MessageSegment.image(photo))
    else:
        await xiaguanzhan_photo.finish("请输入正确的车号!，如：DF7C-5030")

@train_number.handle() #通过车组号查询车次
async def handle_function(args: Message = CommandArg()): # type: ignore
    if number := args.extract_plain_text():  # noqa: F841
        async with httpx.AsyncClient() as client:
            link_train_number = API.api_rail_re + 'emu/' + number.upper()
            response = await client.get(link_train_number)
            data = json.loads(response.text)
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

@train_info.handle() # 通过车次查询列车具体信息，不只是能查询动车组，普速列车也可查询
async def handle_function(args: Message = CommandArg()): # type: ignore
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
            jiaolu_Train_style = stop_time[0]["jiaolu_train_style"] # 车底类型
            jiaolu_Dept_train = stop_time[0]["jiaolu_dept_train"] # 车底配属

            stop_inf = []
            stop_dict = {}

            for stop in stop_time: # 遍历该列车的所有站点、到点、发点、停车时间
                station = stop['stationName']
                arrive_time = time_Formatter(stop['arriveTime'])
                start_time = time_Formatter(stop['startTime'])
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
                station_result += str(station_result_number) + "." + stop['站点'] + "：" + stop['到点'] + "到," + stop['发点'] + "发，停车" + stop['停车时间'] + "\n"
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

@information_helper.handle() #帮助页面
async def handle_function():
    information_Helper_message = Message([
        "这是一个火车迷也许觉得很好用的铁路工具箱，具有多种功能 \n \n",
        "----------使用方法----------\n",
        "① 通过车次查询担当的动车组车组号：/车号 或 /ch （例如：/车号 D3211） \n \n",
        "② 通过动车组车组号查询担当车次：/车次 或 /cc （例如：/车次 CRH2A-2001） \n \n",
        "③ 通过车号查询下关站机车户口照：/下关站 或 /xgz （例如：/下关站 DF7C-5030） \n \n",
        "④ 通过列车车次查询该车次的始发终到、担当客运段、车型信息、配属以及具体时刻表，同时支持动车组与普速列车：/查询 或 /cx （例如：/查询 Z99）\n \n"
        "⑤ 帮助：/帮助 或 /help \n \n",
        "更多功能正在开发中，尽情期待！ \n",
        "------------------------------ \n \n",
        "Powered by Nonebot2 and Onebot v11\n",
        "Copyright © Leaf developer 2023-2025"

    ]) # type: ignore
    
    await information_helper.finish(information_Helper_message)