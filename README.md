# nonebot-plugin-railwaytools

### 这是一个火车迷也许觉得很好用的铁路工具箱，具有多种功能。

#### 项目还在开发中...

## Required 🔨
- Python >= 3.8

- 需提前安装以下依赖库：
```sh
pip install requests
```

## Getting Started 🚀
将本repo中的nonebot-plugin-railwaytools文件夹clone到机器人的src\plugins目录中，即可使用。

```sh
git clone https://github.com/leaf2006/nonebot-plugin-railwaytools.git
```

## Features ✨

- 通过车次查询担当的动车组车组号：/车号 或 /ch （例如：/车号 D3211）
- 通过动车组车组号查询担当车次：/车次 或 /cc （例如：/车次 CRH2A-2001）
- 通过车号查询下关站收录的机车户口照：/下关站 或 /xgz （例如：/下关站 DF7C-5030）
- 帮助：/帮助 或 /help

## Alert ⚠️
由于下关站的性能较差，在查询机车户口照时，返回的图片可能会加载较慢。

## TODO 🔜

- 正在计划给查询机车户口照功能加入显示机车配属与构造速度等信息
- 查询列车始发/终到功能暂未实现
- 如用户的输入内容非法，错误值仅停留在后台而无法通过机器人输出给用户
- 由于下关站的性能问题导致的加载图片较慢，可以通过切换为小图模式解决。但是小图比较模糊，只能说在加载速度快和图片质量高这两者之间只能二选一。本人意向添加切换大/小图的设置选项，但是目前还未开发
- 更多功能正在思考/开发中

## 数据来源 
- 动车组交路数据来源于：https://rail.re
- 机车户口照图片来源于下关站：http://www.xiaguanzhan.com/


Copyright © Leaf developer 2023-2025，遵循MIT开源协议
