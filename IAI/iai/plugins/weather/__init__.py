# coding=utf-8


from nonebot import on_command, CommandSession, get_bot
from nonebot import on_natural_language, NLPSession, NLPResult
from .data_source import get_weather_of_city, get_weather_of_city_HF, should_forecast, get_forecast
from jieba import posseg
from . import data_source
from IAI.iai.common.GroupInfo import get_group_info, update_last_weather_notify
from datetime import datetime, timedelta
from IAI.iai.plugins.DoYouKnow import one_msg


@on_command('weather', aliases=('天气',))
async def weather(session: CommandSession):
    city = session.get('city', prompt='请输入城市')
    ather_report = await get_weather_of_city_HF(city)
    await session.send(ather_report)


@on_command('weather_forecast')
async def weather_forecast(session: CommandSession):
    bot = get_bot()
    if should_forecast(bot.config.DEFAULT_CITY):
        pass


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
    return NLPResult(90.0, 'weather', {'city': city})


@on_command('weather_forecast_hourly')
async def weather_forecast_hourly(session: CommandSession):
    group_info = await get_group_info(session.ctx['group_id'])
    if group_info.last_weather_notify and group_info.last_weather_notify > (datetime.now() - timedelta(hours=6)):
        return

    alert = {}
    for hourly_info in (await data_source.get_weather_hourly(get_bot().config.DEFAULT_CITY))[0:2]:
        if '雨' in hourly_info['cond_txt'] or '雪' in hourly_info['cond_txt']:
            alert['cond'] = hourly_info['cond_txt']
            alert['pop'] = hourly_info['pop']
            await update_last_weather_notify(session.ctx['group_id'], datetime.now())


    if alert:
        one = await one_msg()
        msg = f'''
监测到未来 3 小时内 {get_bot().config.DEFAULT_CITY} 地区可能有降水🌧：

{alert['cond']}
降水概率：{alert['pop']}%

---
{one}'''
        ctx = {'message_type': 'group', 'self_id': get_bot().config.ROBOT_ID, 'group_id': session.ctx['group_id']}
        await get_bot().send(ctx, msg)
