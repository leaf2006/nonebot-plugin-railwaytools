# Copyright © Leaf developer 2023-2026
# 本文件负责实现“通过动车组车次查询车组号”与“通过动车组车组号查询动车组车次”功能

import httpx
import json 
from nonebot import on_command   # type: ignore
from nonebot.adapters.onebot.v11 import Message, MessageSegment   # type: ignore
from nonebot.plugin import PluginMetadata  # type: ignore
from .config import Config
from nonebot.params import CommandArg  # type: ignore
from nonebot.rule import to_me  # type: ignore
from .api import API  

def EMU_code_formatter(str): # 格式化动车组车号 CRH2A2001 -> CRH2A-2001
    return str[:-4] + "-" + str[-4:]

announce = "数据来源：rail.re"

emu_number = on_command("车号",aliases={"ch", "查车号"}, priority=5,block=True)
train_number = on_command("车次",aliases={"cc", "查车次"}, priority=5,block=True)
@emu_number.handle()
async def handle_emu_number(args: Message = CommandArg()): # type: ignore
    if number := args.extract_plain_text():
        async with httpx.AsyncClient(headers=API.headers) as client:
            try:
                link_emu_number = API.api_rail_re + 'train/' + number.upper()
                response = await client.get(link_emu_number)
                data = json.loads(response.text)
                num = len(data)
                count = 0
                final_data = ""
                for i in range(num):
                    if i <= 7:
                        emu_no = EMU_code_formatter(data[i]['emu_no'])
                        date = data[i]['date']
                        final_data += date + '：' + emu_no + "\n"
                        count += 1
                    else:
                        pass

                
                result = Message([
                    number.upper(),"次列车近",str(count),"次担当的车组号为：\n",
                    "------------------------------\n",
                    final_data,
                    "------------------------------\n \n",
                    announce,
                ])

            except json.JSONDecodeError:
                result = "输入的动车组车次格式错误！"
            except Exception as error:
                result = "发生异常，" + error

            await emu_number.finish(result) # type: ignore

    else:
        await emu_number.finish("请输入车号")

@train_number.handle() #通过车组号查询车次
async def handle_train_number(args: Message = CommandArg()): # type: ignore
    if number := args.extract_plain_text():  # noqa: F841
        async with httpx.AsyncClient(headers=API.headers) as client:
            try:
                link_train_number = API.api_rail_re + 'emu/' + number.upper()
                response = await client.get(link_train_number)
                data = json.loads(response.text)
                num = len(data)
                count = 0
                final_data = ""
                for i in range(num):
                    if i <= 7:
                        train_no = data[i]['train_no']
                        date = data[i]['date']
                        final_data += date + '：' + train_no + "\n"
                        count += 1
                    else:
                        pass

                result = Message([
                    "车组号",number.upper(),"近",str(count),"次担当的动车组车次为：\n",
                    "------------------------------\n",
                    final_data,
                    "------------------------------\n \n",
                    announce,
                ])

            except json.JSONDecodeError:
                result = "输入的动车组车组号格式错误！"
            except Exception as error:
                result = "发生异常，" + error

            await train_number.finish(result) # type: ignore
    else:
        await train_number.finish("请输入车次")
