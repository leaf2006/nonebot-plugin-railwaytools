import json
import httpx
import asyncio

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
        url_search = f"{API.api_cnrail_geogv}match_feature/{input_text}?locale=zhcn&query-override" 
        async with httpx.AsyncClient(headers=API.headers) as client:
            res_search = await client.get(url_search)
            res_search_raw_data = json.loads(res_search.text)
            res_search_data = res_search_raw_data['data']
            return res_search_data
            