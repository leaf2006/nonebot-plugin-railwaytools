import json
import requests  
from nonebot import on_command  
from nonebot.adapters.onebot.v11 import Message, MessageSegment  
from nonebot.params import CommandArg  
from nonebot.rule import to_me  

emu_number = on_command("车号", rule=to_me(), aliases={"ch", "查车号"}, priority=1,block=True)
train_number = on_command("车次", rule=to_me(), aliases={"cc", "查车次"}, priority=1,block=True)
information_helper = on_command("help",rule=to_me(),aliases={"帮助"},priority=1,block=True)
xiaguanzhan_photo = on_command("下关站",rule=to_me(),aliases={"xgz"},priority=1,block=True)

@emu_number.handle() #通过车次查询车组号
async def handle_function(args: Message = CommandArg()): # type: ignore
    if number := args.extract_plain_text():  # noqa: F841
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}  # noqa: E501
        link_emu_number = 'https://api.rail.re/train/' + number
        x = requests.get(link_emu_number, headers=headers)
        data = json.loads(x.text)
        num = 0
        final_result = ""
        while num < 8:
            result = data[num]['emu_no']
            time = data[num]['date']
            final_result += time + '：' +result + "\n"
            num += 1
            print_out = number + '次列车近8次担当的车组号为：\n' + final_result
        await emu_number.finish(print_out) # type: ignore

    else:
        await emu_number.finish("请输入车号")


@train_number.handle() #通过车组号查询车次
async def handle_function(args: Message = CommandArg()): # type: ignore
    if number := args.extract_plain_text():  # noqa: F841
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}  # noqa: E501
        link_train_number = 'https://api.rail.re/emu/' + number
        x = requests.get(link_train_number, headers=headers)
        data = json.loads(x.text)
        num = 0
        final_result = ""
        while num < 8:
            result = data[num]['train_no']
            time = data[num]['date']
            final_result += time + '：' +result + "\n"
            num += 1
            print_out = number + '近8次担当的车次为：\n' + final_result
        await train_number.finish(print_out) # type: ignore

    else:
        await train_number.finish("请输入车次")

@xiaguanzhan_photo.handle() #查询下关站列车户口照
async def handle_function(args: Message = CommandArg()): # type: ignore
    # 提取参数纯文本作为地名，并判断是否有效
    if number := args.extract_plain_text():
        await xiaguanzhan_photo.send("正在加载图片，时间可能略久...")
        link_xiaguanzhan = "http://www.xiaguanzhan.com/uploadfiles/"
        photo = link_xiaguanzhan + number + ".jpg"
        await xiaguanzhan_photo.finish(MessageSegment.image(photo))
    else:
        await xiaguanzhan_photo.finish("请输入正确的车号!，如：DF7C-5030")

@information_helper.handle() #帮助页面
async def handle_function():
    information_Helper_message = Message([
        "这是一个火车迷也许觉得很好用的铁路工具箱，具有多种功能 \n \n",
        "----------使用方法----------\n",
        "① 通过车次查询担当的动车组车组号：/车号 或 /ch （例如：/车号 D3211） \n \n",
        "② 通过动车组车组号查询担当车次：/车次 或 /cc （例如：/车次 CRH2A-2001） \n \n",
        "③ 通过车号查询下关站图片：/下关站 或 /xgz （例如：/下关站 DF7C-5030） \n \n",
        "④ 帮助：/帮助 或 /help \n \n",
        "更多功能正在开发中，尽情期待！ \n",
        "------------------------------ \n \n",
        "Powered by Nonebot2 and Onebot v11\n",
        "Copyright © Leaf developer 2023-2025"

    ]) # type: ignore

    await information_helper.finish(information_Helper_message)