"""
IAIbot 初始化模块
初始化系统，连接数据库，加载插件

author: 16030199025 张俊华
"""

from os import path
import sys
import setup
import os

import nonebot as none

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import IAI.iai.common.cache as cache



if __name__ == '__main__':
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
    none.init(setup)

    bot = none.get_bot()
    bot.server_app.before_serving(cache.init)

    none.load_builtin_plugins()
    none.load_plugins(path.join(path.dirname(__file__), 'iai', 'plugins'),
                      'iai.plugins')
    none.run()
