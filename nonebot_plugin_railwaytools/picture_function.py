# Copyright © Leaf developer 2023-2026
# 本文件负责实现“查询下关站机车车号”功能

import httpx
from httpx import AsyncClient 
from nonebot import on_command   # type: ignore
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment   # type: ignore
from nonebot.params import CommandArg  # type: ignore
from nonebot.rule import to_me  # type: ignore
from .utils import utils
from .api import API  

xiaguanzhan_photo = on_command("下关站",aliases={"xgz"},priority=5,block=True)
EMU_route_schedule = on_command("交路表",aliases={"jlb"},priority=5,block=True)

@xiaguanzhan_photo.handle() #查询下关站列车户口照
async def handle_xiaguanzhan_photo(event:Event, args: Message = CommandArg()): # type: ignore
    raw_message = str(event.get_message()).strip()
    command_part = utils.get_command_part(raw_message)
    valid_commands = ['下关站','xgz']
    if command_part not in valid_commands:
        return

    if number := args.extract_plain_text():
        await xiaguanzhan_photo.send("正在加载图片，时间可能略久...")
        async with httpx.AsyncClient(headers=API.headers, timeout=30.0) as client:
            data = {
                "keyword": number
            }
            xiaguanzhan_resp = await client.post(API.api_xiaguanzhan, data=data)
            xiaguanzhan_resp.encoding = "gb2312"
        # 获取基本信息
        first_match = utils.xiaguanzhan_first_match
        title = first_match(r'<h1><span class="blue"><a href="ProView\.asp\?ProId=[^"]*" title="[^"]*" target="_blank">(.*?)</a></span></h1>', xiaguanzhan_resp.text)
        if title == None:
            await xiaguanzhan_photo.finish(f"暂无{number}的信息")
        manufacturer = first_match(r'生产厂商：(.*?)<BR>', xiaguanzhan_resp.text)
        shoot_date = first_match(r'拍摄日期：(.*?)<BR>', xiaguanzhan_resp.text)
        shoot_author = first_match(r'拍摄作者：(.*?)</FONT>', xiaguanzhan_resp.text)
        photo_url = first_match(r'下载地址：<a href="(.*?)" target="_blank">', xiaguanzhan_resp.text)

        title_separate = title.split(' ')
        locomotive_no = title_separate[1]
        locomotive_allocation = title_separate[2]

        xiaguanzhan_photo_output = Message ([
            MessageSegment.image(photo_url),
            f"【{locomotive_no}】\n",
            f"配属：{locomotive_allocation}\n",
            f"生产厂商：{manufacturer}\n",
            f"拍摄日期：{shoot_date}\n",
            f"拍摄作者：{shoot_author}\n\n",
            "数据来源：下关站-铁路摄影馆",
        ])
        await xiaguanzhan_photo.finish(xiaguanzhan_photo_output)

    else:
        await xiaguanzhan_photo.finish("请输入正确的车号!，如：HXD1D-1898")

@EMU_route_schedule.handle() # 获取动车组交路表，还是来源于rail.re
async def handle_EMU_route_schedule(event:Event, args: Message = CommandArg()):
    raw_message = str(event.get_message()).strip()
    command_part = utils.get_command_part(raw_message)
    valid_commands = ['交路表','jlb']
    if command_part not in valid_commands:
        return
    
    if train_Number_input := args.extract_plain_text():
        res_EMU_route_schedule = API.api_EMU_route_schedule + train_Number_input.upper() + ".png"
        EMU_Route_schedule_result = Message([
            MessageSegment.image(res_EMU_route_schedule),
            f"【{train_Number_input.upper()}次】动车组列车交路表 \n",
            "⚠本功能还处于测试中⚠ \n 交路表来源：rail.re，部分运行图数据可能已经过时，仅供参考！",
        ])
        
        await EMU_route_schedule.finish(EMU_Route_schedule_result)
    
    else:
        await EMU_route_schedule.finish("请输入正确的动车组车次!，如：D3211")