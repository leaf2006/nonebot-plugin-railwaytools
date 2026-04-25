import re
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
    
    def decrypt_cnrail_data(encrypted_str: str) -> dict:
        """
        解密 cnrail.geogv.org API 返回的混淆字符串
        """

        # 如果最外层包着多余的引号，先通过 json.loads 脱掉引号转为正常的内部字符串
        if encrypted_str.startswith('"') and encrypted_str.endswith('"'):
            try:
                encrypted_str = json.loads(encrypted_str)
            except json.JSONDecodeError:
                pass
        
        if not encrypted_str:
            return "ERR"
        
        key_length = ord(encrypted_str[0]) # 第一位字符的 ASCII 码值代表密钥的长度，如结果为\u0007则提取为7
        key = encrypted_str[1:1+key_length] # 紧接着的key_length个字符是密钥
        payload = encrypted_str[1+key_length:] # 剩下的都是加密过的密文

        # 解密部分
        decrypted_chars = []
        for i, char in enumerate(payload):
            key_char = key[i % len(key)]

            # 密文字符 ASCII - 密钥字符 ASCII = 原文字符 ASCII
            decrypted_char_code = ord(char) - ord(key_char)
            decrypted_chars.append(chr(decrypted_char_code)) # 由ASCII解密为普通字符串
        
        decrypted_str = "".join(decrypted_chars)

        try:
            return json.loads(decrypted_str)
        except json.JSONDecodeError:
            return "ERR"
    
    def xiaguanzhan_first_match(pattern, text):
        m = re.search(pattern, text, re.IGNORECASE)
        return m.group(1).strip() if m else None

