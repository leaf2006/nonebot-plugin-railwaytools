# Copyright © Leaf developer 2023-2026
# 本文件负责实现“列车查询”功能，部分灵感来源于GitHub项目https://github.com/zmy15/ChinaRailway，特此注明

import json
import datetime  
import httpx
from nonebot import on_command   # type: ignore
from nonebot.adapters.onebot.v11 import Message, MessageSegment   # type: ignore
from nonebot.plugin import PluginMetadata  # type: ignore
from nonebot.params import CommandArg  # type: ignore
from nonebot.rule import to_me  # type: ignore
from .utils import utils
from .api import API  

train_info = on_command("列车查询",aliases={"cx","查询"},priority=5,block=True)


@train_info.handle() # 通过车次查询列车具体信息，不只是能查询动车组，普速列车也可查询
async def handle_train_info(args: Message = CommandArg()): # type: ignore
    if train_number_input := args.extract_plain_text(): 

        is_real_time_query = False # 默认参数为False

        if "-" in train_number_input: # /查询 功能的二级参数
            if "-实时" in train_number_input:
                is_real_time_query = True # 判断是否启用实时信息查询（列车当前到达何车站，正晚点情况）

            train_number_input = train_number_input.split("-")[0].strip() # 提取“-”前的字符串
        else:
            pass 

        async with httpx.AsyncClient(headers=API.headers) as client:

            toDay = datetime.date.today().strftime("%Y%m%d") #获取今日时间，以%Y%m%d的格式形式输出
            yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")
            tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y%m%d")
            the_day_before_yesterday = (datetime.date.today() - datetime.timedelta(days=2)).strftime("%Y%m%d")
            the_day_after_tomorrow = (datetime.date.today() + datetime.timedelta(days=2)).strftime("%Y%m%d")
            
            request_dates = toDay

            try:
                
                # 增加对于列车当日是否开行的判断。判断方法如下：
                # 查询该列车当日的信息，如果无返回数据，则查询±1天与±2天的数据，如都没有，就是没有或长期停开；如果有，则输出那几天的数据，并注明“该列车当日不开行”
                for i in range(5):
                    info_data = {
                        "trainCode" : train_number_input.upper(),
                        "startDay" : request_dates
                    }
                    info_res = await client.post(API.api_12306,data=info_data)
                    info_response_data = json.loads(info_res.text) # 对返回数据进行处理
                    request_details = info_response_data['data']['trainDetail'] 

                    if not request_details and request_dates == toDay:
                        request_dates = yesterday
                    elif not request_details and request_dates == yesterday:
                        request_dates = tomorrow
                    elif not request_details and request_dates == tomorrow:
                        request_dates = the_day_before_yesterday
                    elif not request_details and request_dates == the_day_before_yesterday:
                        request_dates = the_day_after_tomorrow
                    else:
                        break

                # 对返回数据进行分析
                stop_time = info_response_data['data']['trainDetail']['stopTime']

                train_code = stop_time[0]['stationTrainCode'] # 车次
                start_station_name = stop_time[0]['start_station_name'] # 始发站名
                end_station_name = stop_time[0]['end_station_name'] # 终到站名

                jiaolu_corporation_code = stop_time[0]["jiaolu_corporation_code"] # 担当客运段
                if info_data["trainCode"][0] == "D" or info_data["trainCode"][0] == "G" or info_data["trainCode"][0] == "C":
                    # url_emu_code = API.api_rail_re + "train/" + info_data["trainCode"]
                    url_emu_code = f"{API.api_rail_re}train/{train_code}"
                    res_info_EMU = await client.get(url_emu_code)
                    info_EMU_code = json.loads(res_info_EMU.text)
                    if res_info_EMU.status_code == 404 or not info_EMU_code:
                        jiaolu_train_style = " " # Bug fix：判断rail.re的数据库里有没有这个车次的信息，没有的话就给车型信息赋一个空的值
                    else:
                        if info_EMU_code[0]['date'] == info_EMU_code[1]['date']: # 判定是否重联
                            jiaolu_train_style = f"{utils.EMU_code_formatter(info_EMU_code[0]['emu_no'])}与{utils.EMU_code_formatter(info_EMU_code[1]['emu_no'])}重联"
                        else:
                            jiaolu_train_style = utils.EMU_code_formatter(info_EMU_code[0]['emu_no'])

                else:
                    jiaolu_train_style = stop_time[0]["jiaolu_train_style"] # 车底类型（普通车）

                jiaolu_dept_train = stop_time[0]["jiaolu_dept_train"] # 车底配属

                if request_dates == toDay:
                    train_schedule_info = f"{train_code}次{datetime.date.today().strftime("%m月%d日")}{start_station_name}方面正常开行"
                else:
                    train_schedule_info = f"{train_code}次{datetime.date.today().strftime("%m月%d日")}{start_station_name}方面不开行或已停运，请关注车站公告"

                stop_inf = []
                stop_dict = {}


                for i, stop in enumerate(stop_time): # 遍历该列车的所有站点、到点、发点、停车时间
                    station = stop['stationName']
                    arrive_time = utils.time_Formatter_1(stop['arriveTime'])
                    start_time = utils.time_Formatter_1(stop['startTime'])
                    stopover_time = stop['stopover_time'] + "分"
                    ticketDelay = stop['ticketDelay']
                    day_difference = stop['dayDifference']
                    stop_time_count = len(stop_time)

                    if i == 0: # 判断始发/终到站，给不存在的到点/发点变成“--:--”
                        arrive_time = "--:--"
                        stopover_time = "--分" 
                    elif i == stop_time_count -1:
                        start_time = "--:--"
                        stopover_time = "--分"
                    else:
                        pass

                    if is_real_time_query == True:
                        stop_dict.setdefault("晚点",ticketDelay)
                    else:
                        pass
                    
                    stop_dict.setdefault("站点",station)
                    stop_dict.setdefault("到点",arrive_time)
                    stop_dict.setdefault("发点",start_time)
                    stop_dict.setdefault("停车时间",stopover_time)
                    stop_dict.setdefault("day_difference",day_difference)
                    stop_inf.append(stop_dict)
                    stop_dict = {}

                if is_real_time_query == True:
                    now_time = datetime.datetime.now().strftime("%H:%M")
                    end_station_count = stop_time_count - 1
                    now_station_count = 0
                    train_arrival_status = ""
                    if now_time < utils.time_Formatter_1(stop_time[0]['startTime']):
                        train_arrival_status = "列车始发站待发"
                    elif now_time > utils.time_Formatter_1(stop_time[end_station_count]['arriveTime']) and stop_time[end_station_count]['dayDifference'] == 0:
                        train_arrival_status = "列车已经到达终点站"
                        now_station_count = end_station_count
                    else:
                        for station in range(stop_time_count-1):
                            if utils.time_Formatter_1(stop_time[station]['startTime']) < now_time and utils.time_Formatter_1(stop_time[station + 1]['arriveTime']) > now_time:
                                now_station = stop_time[station + 1]['stationName']
                                train_arrival_status = f"列车正在前往{now_station}站"
                                now_station_count = station
                                break
                else:
                    train_arrival_status = ""

                station_result = ""
                count = 1 # 给时刻表标上序号
                # day_difference_buffer = 0
                # day_differences = [int(stop.get('day_difference', 0)) for stop in stop_inf]
                for i,stop in enumerate(stop_inf): # 想办法整出时刻表的结果，最后将结果添加到Message中去
                    # day_difference_output = ""

                    if is_real_time_query == True:
                        if request_dates != toDay:
                            delay = ""
                        else:
                            if stop['晚点'] == "0" and i <= now_station_count:
                                delay = "，正点运行"
                            elif stop['晚点'] == "0" and i > now_station_count:
                                delay = "，预计正点"
                            else:
                                delay = f"，晚点{stop['晚点']}分"

                    else:
                        delay = ""

                    # current_day_diff = day_differences[i]
                    # next_day_diff = day_differences[i+1] if i+1 < len(day_differences) else current_day_diff
                    # if current_day_diff != day_difference_buffer:
                    #     day_difference_buffer = current_day_diff
                    #     day_difference_output = f"（+{day_difference_buffer}天）\n"
                    
                    station_result += str(count) + "." + stop['站点'] + "：" + stop['到点'] + "到," + stop['发点'] + "开，停车" + stop['停车时间'] + delay + "\n"
                    count += 1

                train_info_output = Message([ # 结果Message
                    "车次：",train_code,
                    "（",start_station_name , "——" , end_station_name , ") \n",
                    "担当客运段：" , jiaolu_corporation_code , "\n",
                    "车型信息：" , jiaolu_train_style , "\n",
                    "配属：" , jiaolu_dept_train , "\n",
                    train_schedule_info , "\n",
                    train_arrival_status , "\n",
                    "----------停站信息----------\n",
                    station_result,
                    "------------------------------ \n \n",
                    "数据来源：12306",
                ]) # type: ignore

            except KeyError:
                # train_info_output = "输入车次格式错误或者车次未收录，亦又可能是该车次近日不开行。请重新输入！"
                train_info_output = Message([
                    "您输入的车次",train_number_input.upper(),"无法查询，可能是以下两种原因导致：\n",
                    "------------------------------ \n",
                    "1.输入车次格式错误或者车次未收录 \n",
                    "2.该车次近期不开行 \n",
                    "------------------------------ \n",
                    "请重新输入！",
                ])
            except Exception as error:
                train_info_output = "发生异常：" + str(error)

            await train_info.finish(train_info_output)
             

    else:
        await train_info.finish("请输入正确的列车车次！（如：Z225）")
