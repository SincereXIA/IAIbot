from aip import AipNlp
from IAI.setup import *
APP_ID = str(11705272)
API_KEY = str(BD_API_KEY)
SECRET_KEY = str(BD_SECRET_KEY)

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

text = "你去死吧"
text0 = '周5啥课'
tests = ['星期二上什么课','下午上什么课','今天上什么课','明天上什么课','明天下午什么课','下周二下午什么课']
""" 调用词法分析 """
for text in tests:
    c = client.lexer(text)

rs = client.sentimentClassify(text)
for text in tests:
    print(client.simnet(text0,text))



