# Copyright © Leaf developer 2023-2026
# 本文件负责实现“查询下关站机车车号”功能

import httpx 
from nonebot import on_command   # type: ignore
from nonebot.adapters.onebot.v11 import Message, MessageSegment   # type: ignore
from nonebot.plugin import PluginMetadata  # type: ignore
from .config import Config
from nonebot.params import CommandArg  # type: ignore
from nonebot.rule import to_me  # type: ignore
from .api import API  

xiaguanzhan_photo = on_command("下关站",aliases={"xgz"},priority=5,block=True)

@xiaguanzhan_photo.handle() #查询下关站列车户口照
async def handle_xiaguanzhan_photo(args: Message = CommandArg()): # type: ignore
    if number := args.extract_plain_text():
        await xiaguanzhan_photo.send("正在加载图片，时间可能略久...")
        photo = API.api_xiaguanzhan + number + ".jpg"
        await xiaguanzhan_photo.finish(MessageSegment.image(photo))
    else:
        await xiaguanzhan_photo.finish("请输入正确的车号!，如：DF7C-5030")