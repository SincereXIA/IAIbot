# coding=utf-8


from none import  on_command, CommandSession
from none import on_natural_language, NLPSession, NLPResult
from .data_source import get_weather_of_city, get_weather_of_city_HF
from jieba import posseg
import nlp
import sys
print(sys.path)

@on_command('weather', aliases=('天气',))
async def weather(session: CommandSession):

    city = session.get('city', prompt='请输入城市')
    ather_report = await get_weather_of_city_HF(city)

    await session.send(ather_report)

@weather.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.current_key:
        session.args[session.current_key] = stripped_arg

    elif stripped_arg:
        session.args['city'] = stripped_arg

# on_natural_language 装饰器将函数声明为一个自然语言处理器
# keywords 表示需要响应的关键词，类型为任意可迭代对象，元素类型为 str
# 如果不传入 keywords，则响应所有没有被当作命令处理的消息
@on_natural_language(keywords=('天气',))
async def _(session: NLPSession):
    stripped_msg_text = session.msg_text.strip()
    words = posseg.lcut(stripped_msg_text)
    city = None
    # 返回处理结果，3 个参数分别为置信度、命令名、命令会话的参数
    for word in words:
        if word.flag == 'ns':
            city = word.word
    await session.send('NLP 处理成功')
    return NLPResult(90.0, 'weather', {'city':city})


