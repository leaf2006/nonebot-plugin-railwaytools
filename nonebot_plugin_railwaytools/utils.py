import json
import httpx
import asyncio
import traceback

from .api import API

class utils:
    """存放各类需要的def定义"""
    def time_Formatter_1(time) -> str:
        """格式化时间，1145 -> 11:45"""
        return time[:2] + ":" + time[2:]

    def time_Formatter_2(time) -> str:
        """格式化时间，2025-12-17 14:50:00 -> 14:50"""
        return time[11:16]
    def EMU_code_formatter(str):
        """格式化动车组车号 CRH2A2001 -> CRH2A-2001"""
        return str[:-4] + "-" + str[-4:]

    async def cnrail_search(input_text):
        """cnrail的搜索模块，获取rail id必用"""
        url_search = f"{API.api_cnrail_geogv}search?keyword={input_text}" 
        async with httpx.AsyncClient(headers=API.headers) as client:
            res_search = await client.get(url_search)
            res_search_data = json.loads(res_search.text) # Fixed:适配新版api调用方式
            return res_search_data
        
    def get_command_part(raw_message):
        """
        获取命令部分
        """
        space_index = raw_message.find(' ') # 找到空格所在的位置（空格用于分隔指令与参数）
        if space_index != -1:
            command_part = raw_message[:space_index]
        else:
            command_part = raw_message
        
        command_part = command_part.replace('/','')
        return command_part
    
    def short_tb(exc: Exception) -> str:
        """
        用于精简TraceBack
        """
        te = traceback.TracebackException.from_exception(exc)
        if te.stack:
            last = te.stack[-1]
            # 只保留最后一帧
            frame = f'File "{last.filename}", line {last.lineno}, in {last.name}\n    {last.line}'
        else:
            frame = "No traceback frame"
        exc_only = "".join(te.format_exception_only()).strip()
        return f"{frame}\n{exc_only}"