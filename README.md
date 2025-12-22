<div align="center">
    <a href="https://v2.nonebot.dev/store">
        <img src="https://cdn.jsdelivr.net/gh/leaf2006/image/img/nb_plugin_railwaytools.png">
    </a>

# nonebot-plugin-railwaytools

<!-- ![GitHub Repo stars](https://img.shields.io/github/stars/leaf2006/nonebot-plugin-railwaytools) -->
![GitHub Repo stars](https://img.shields.io/github/stars/leaf2006/nonebot-plugin-railwaytools?style=flat-square)
![GitHub License](https://img.shields.io/github/license/leaf2006/nonebot-plugin-railwaytools?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/leaf2006/nonebot-plugin-railwaytools?style=flat-square)
![Static Badge](https://img.shields.io/badge/Python-%3E%3D3.8-blue?style=flat-square)
![PyPI - Version](https://img.shields.io/pypi/v/nonebot-plugin-railwaytools?style=flat-square)





</div>



### 这是一个火车迷也许觉得很好用的铁路工具箱，具有多种功能。

## Required 🔨
- Python >= 3.8

- 需提前安装以下依赖库：
```sh
pip install httpx
```

## Getting Started 🚀

- 1.使用 nb-cli 安装：在 nonebot2 项目的根目录下打开命令行，输入以下指令即可安装

```sh
nb plugin install nonebot-plugin-railwaytools
```

- 2.可通过pip安装该插件

```sh
pip install nonebot-plugin-railwaytools
```

- 2.将本repo中的nonebot-plugin-railwaytools文件夹clone到机器人的src\plugins目录中，即可使用。

```sh
git clone https://github.com/leaf2006/nonebot-plugin-railwaytools.git
```

## Features ✨

- 通过车次查询担当的动车组车组号：/车号 [动车组车次] 或 /ch [动车组车次]（例如：/车号 D3211）
```
example：
🤵：/车号 D3211
🤖：
D3211次列车近8次担当的车组号为：
2025-11-28 12:59：CRH2A2158
2025-11-27 12:59：CRH2A2190
2025-11-26 12:59：CRH2A2158
2025-11-25 12:59：CRH2A2030
2025-11-24 12:59：CRH2B2115
2025-11-23 12:59：CRH2B2116
2025-11-22 12:59：CRH2B2115
2025-11-21 12:59：CRH2A2006
```

- 通过动车组车组号查询担当车次：/车次 [动车组车组号] 或 /cc [动车组车组号]（例如：/车次 CRH2A-2001）
```
example：
🤵：/车次 CRH2A-2001
🤖：
CRH2A-2001近8次担当的车次为：
2025-11-28 20:14：D2212
2025-11-27 22:46：D3062
2025-11-27 15:05：D3060
2025-11-26 20:22：C3793
2025-11-26 13:57：D5666
2025-11-26 10:09：D5665
2025-11-25 17:29：C3896
2025-11-25 12:36：C3897
```

- 通过车号查询下关站收录的机车户口照：/下关站 [机车车号] 或 /xgz [机车车号] （例如：/下关站 DF7C-5030）
```
example:
🤵：/下关站 DF7C-5058
🤖：正在加载图片，时间可能略久...
🤖：[DF7C-5058的机车户口照]
```

- 通过列车车次查询该车次的始发终到、担当客运段、车型信息以及配属，同时支持动车组与普速列车：/查询 [列车车次] 或 /cx [列车车次] （例如：/查询 Z99）
```
example:
🤵：/查询 Z99
🤖：
车次：Z99（上海——广州白云) 
担当客运段：上海客运段
车型信息：25T
配属：上海机辆段
 
----------停站信息----------
1.上海：17:19到,17:19发，停车0分
2.杭州南：19:26到,19:29发，停车3分
3.金华：20:40到,20:46发，停车6分
4.广州白云：09:45到,09:45发，停车0分
------------------------------
```

- 通过车站名称查看车站大屏：/大屏 [车站名称] 或 /dp [车站名称] （例如：/大屏 上海）
```
example:
🤵：/大屏 上海
🤖：
【上海站】车站大屏如下：
 
------------------------------ 
【1】G7020（上海——南京）16:00开 ， 状态：停止检票 
【2】K372（上海——大同）16:03开 ， 状态：正在检票 
【3】G7632（上海——黄山北）16:13开 ， 状态：正点 
【4】G8274（上海——徐州东）16:18开 ， 状态：正点 
【5】G2818（上海——武汉）16:22开 ， 状态：正点 
【6】T110（上海——北京）16:30开 ， 状态：正点 
【7】G7076（上海——合肥南）16:41开 ， 状态：正点 
【8】C3892（上海——扬州）16:42开 ， 状态：正点 
【9】Z40（上海——乌鲁木齐）16:48开 ， 状态：正点 
【10】G7222（上海——合肥）16:49开 ， 状态：正点 
------------------------------ 
 
仅显示该车站部分列车信息。本车站大屏来源于第三方API，及供参考，请勿用于实际乘车！
数据刷新时间：2025-12-17 16:08:02
```

- 帮助：/帮助 或 /help
```
example:
🤵：/help
🤖：
这是一个火车迷也许觉得很好用的铁路工具箱，具有多种功能 
 
----------使用方法----------
① 通过车次查询担当的动车组车组号：/车号 或 /ch （例如：/车号 D3211） 
 
② 通过动车组车组号查询担当车次：/车次 或 /cc （例如：/车次 CRH2A-2001） 
 
③ 通过车号查询下关站机车户口照：/下关站 或 /xgz （例如：/下关站 DF7C-5030） 
 
④ 通过列车车次查询该车次的始发终到、担当客运段、车型信息以及配属，同时支持动车组与普速列车：/查询 或 /cx （例如：/查询 Z99）

⑤ 通过车站名称查看车站大屏：/大屏 或 /dp （例如：/大屏 上海）
 
⑥ 帮助：/帮助 或 /help 
 
更多功能正在开发中，尽情期待！ 
------------------------------ 
 
Powered by Nonebot2 and Onebot v11
Copyright © Leaf developer 2023-2025
```

## Features(Testing)🚨

#### 列在此处的功能正在测试，仅会在GitHub发布的测试版本中出现，不会加入到机器人的/help菜单中，也不会作为正式版发布到Pypi。这些功能后续可能会在证实稳定且实用后加入正式版中，也有可能会因不可行而被移除。

- 查询rail.re动车组交路表（几行代码实现的很简单的功能）：/交路表 [动车组车次] 或 /jlb [动车组车次]


## Alert ⚠️
- 由于下关站的性能较差，在查询机车户口照时，返回的图片可能会加载较慢。

- 在许多功能上如用户的输入内容非法，错误值仅停留在后台而无法通过机器人输出给用户。这是目前已知问题，正在计划修复（实际是本人比较懒）

## TODO 🔜

- 计划加入生成模拟列车检票大屏的图片的功能，类似CRsim的这种
- ~~计划加入12306车站大屏功能~~ **（已实现）**
- ~~正在计划加入12306查询列车始发终到、中途停站的功能~~ **（已实现）**
- 优化列车时刻表的显示，比如说始发站不要显示到站时间，很怪异。目前可以看作是一个已知的bug
- 如用户的输入内容非法，错误值仅停留在后台而无法通过机器人输出给用户
- 由于下关站的性能问题导致的加载图片较慢，可以通过切换为小图模式解决。但是小图比较模糊，只能说在加载速度快和图片质量高这两者之间只能二选一。本人意向添加切换大/小图的设置选项，但是目前还未开发
- 更多功能正在思考/开发中

## 数据来源 
- 动车组交路数据来源于：https://rail.re
- 机车户口照图片来源于下关站：http://www.xiaguanzhan.com/
- 列车查询数据来源于12306


<div align="center">

Copyright © Leaf developer 2023-2026，遵循MIT开源协议

</div>