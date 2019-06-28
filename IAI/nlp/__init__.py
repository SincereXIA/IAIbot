"""
IAIbot 自然语言处理
调用Jieba分词，百度自然语言 API，完成自然语言信息的提取

author: 16030199025 张俊华
"""
from aip import AipNlp
from IAI.setup import *
APP_ID = str(11705272)
API_KEY = str(BD_API_KEY)
SECRET_KEY = str(BD_SECRET_KEY)

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

