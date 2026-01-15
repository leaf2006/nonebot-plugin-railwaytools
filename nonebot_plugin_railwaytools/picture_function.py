# Copyright © Leaf developer 2023-2026
# 本文件负责实现“查询下关站机车车号”功能

import httpx
from httpx import AsyncClient 
from nonebot import on_command   # type: ignore
from nonebot.adapters.onebot.v11 import Message, MessageSegment   # type: ignore
from nonebot.plugin import PluginMetadata  # type: ignore
from nonebot.params import CommandArg  # type: ignore
from nonebot.rule import to_me  # type: ignore
from .api import API  

xiaguanzhan_photo = on_command("下关站",aliases={"xgz"},priority=5,block=True)
EMU_route_schedule = on_command("交路表",aliases={"jlb"},priority=5,block=True)

@xiaguanzhan_photo.handle() #查询下关站列车户口照
async def handle_xiaguanzhan_photo(args: Message = CommandArg()): # type: ignore
    if number := args.extract_plain_text():
        await xiaguanzhan_photo.send("正在加载图片，时间可能略久...")
        photo = API.api_xiaguanzhan + number + ".jpg"
        await xiaguanzhan_photo.finish(MessageSegment.image(photo))
    else:
        await xiaguanzhan_photo.finish("请输入正确的车号!，如：DF7C-5030")

@EMU_route_schedule.handle() # 获取动车组交路表，还是来源于rail.re
async def handle_EMU_route_schedule(args: Message = CommandArg()):
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