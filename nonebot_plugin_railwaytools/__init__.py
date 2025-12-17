# Copyright © Leaf developer 2023-2026
# 代码写的一坨屎，轻点喷qwq
# 这里是本插件的__init__入口

from nonebot import on_command   # type: ignore
from nonebot.adapters.onebot.v11 import Message, MessageSegment   # type: ignore
from nonebot.plugin import PluginMetadata  # type: ignore
from .config import Config
from nonebot.params import CommandArg  # type: ignore
from nonebot.rule import to_me  # type: ignore
from .emu_function import handle_emu_number , handle_train_number
from .xiaguan_photo import handle_xiaguanzhan_photo
from .train_info import handle_train_info
from .station_screen import handle_station_screen

# 插件配置页
__plugin_meta__ = PluginMetadata(
    name="火车迷铁路工具箱",
    description="这是一个火车迷也许觉得很好用的铁路机器人工具箱",
    usage="""
    /车号 [动车组车次] - 通过车次查询担当的动车组车组号
    /车次 [动车组车组号] - 通过动车组车组号查询担当车次
    /下关站 [机车车号] - 通过车号查询下关站机车户口照
    /查询 [列车车次] - 通过列车车次查询该车次的始发终到、担当客运段、车型信息、配属以及具体时刻表
    /大屏 [车站名称] - 通过车站名称查看车站大屏
    /help - 查看帮助信息
    """,

    type="application",
    # 发布必填，当前有效类型有：`library`（为其他插件编写提供功能），`application`（向机器人用户提供功能）。

    homepage="https://github.com/leaf2006/nonebot-plugin-railwaytools",
    # 发布必填。

    config=Config,
    # 插件配置项类，如无需配置可不填写。

    supported_adapters={"~onebot.v11"},
    # 支持的适配器集合，其中 `~` 在此处代表前缀 `nonebot.adapters.`，其余适配器亦按此格式填写。
    # 若插件可以保证兼容所有适配器（即仅使用基本适配器功能）可不填写，否则应该列出插件支持的适配器。
)

information_helper = on_command("help",aliases={"帮助"},priority=6,block=True)
@information_helper.handle() #帮助页面
async def handle_information_helper():
    information_Helper_message = Message([
        "这是一个火车迷也许觉得很好用的铁路工具箱，具有多种功能 \n \n",
        "----------使用方法----------\n",
        "① 通过车次查询担当的动车组车组号：/车号 或 /ch （例如：/车号 D3211） \n \n",
        "② 通过动车组车组号查询担当车次：/车次 或 /cc （例如：/车次 CRH2A-2001） \n \n",
        "③ 通过车号查询下关站机车户口照：/下关站 或 /xgz （例如：/下关站 DF7C-5030） \n \n",
        "④ 通过列车车次查询该车次的始发终到、担当客运段、车型信息、配属以及具体时刻表，同时支持动车组与普速列车：/查询 或 /cx （例如：/查询 Z99）\n \n"
        "⑤ 通过车站名称查看车站大屏：/大屏 或 /dp （例如：/大屏 上海）\n \n"
        "⑥ 帮助：/帮助 或 /help \n \n",
        "更多功能正在开发中，尽情期待！ \n",
        "------------------------------ \n \n",
        "Powered by Nonebot2 and Onebot v11\n",
        "Copyright © Leaf developer 2023-2026"

    ]) # type: ignore
    
    await information_helper.finish(information_Helper_message)