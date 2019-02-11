import nonebot
from nonebot import session, CommandSession, on_command, get_bot
from . import data_source, message
from IAI.iai.plugins.weather.data_source import get_today_weather_info
from datetime import datetime,date
from IAI.iai.common.QQUser import get_user_group
from IAI.iai.plugins.DoYouKnow.data_source import get_one_content,get_news
from IAI.iai.plugins.DoYouKnow import news_msg
from nonebot.helpers import render_expression

@on_command('morning_call')
async def one(session: CommandSession):
    DEFAULT_CITY = get_bot().config.DEFAULT_CITY
    if 'city' not in session.args.keys():
        session.args['city'] = DEFAULT_CITY
    weather = await get_today_weather_info(session.args['city'])

    one = await one_msg()

    weekday = ['一', '二', '三', '四', '五', '六', '日']
    date = datetime.now().strftime("%m ") + '月' + datetime.now().strftime(" %d")

    class_info = "今天的课程有："

    # 获取用户群信息
    if 'group_id' in session.ctx.keys():
        group_id = session.ctx['group_id']
    else:
        group_id = await get_user_group(session.ctx['user_id'])

    classes = await data_source.get_today_class_info(group_id)
    group_name = ""
    for c in classes:
        class_info += message.morningcall_class_msg.format(
            class_num=c['class_num'],
            class_name=c['class_name']
        )

    msg = message.morningcall_msg.format(
        **{'date': date,
           'weekday': weekday[datetime.now().weekday()],
           'weather': weather['cond_d'],
           'tmp_max': weather['tmp_max'],
           'tmp_min': weather['tmp_min'],
           'class': class_info,
           'comf': weather['comf'],
           'drsg': weather['drsg'],
           'one': one,
           })
    await session.send(msg)


@on_command('one')
async def one(session: CommandSession):
    data = await get_one_content()
    msg = f'''
    {data['text']}
    —— {data['info']}
    '''
    await session.send(msg)


async def one_msg():
    data = await get_one_content()
    msg = f'''
    「{data['text']}」
    —— {data['info']}
        '''
    return msg


@on_command('news')
async def one(session: CommandSession):
    msg = await news_msg()
    await session.send(msg)


@on_command('morning_love')
async def morning_love(session: CommandSession):
    DEFAULT_CITY = "随州"
    CITY_HOME1 = "太原"
    CITY_HOME2 = "西安"

    weather = await get_today_weather_info(DEFAULT_CITY)
    weather1 = await get_today_weather_info(CITY_HOME1)
    weather2 = await get_today_weather_info(CITY_HOME2)


    one = await one_msg()

    weekday = ['一', '二', '三', '四', '五', '六', '日']
    date = datetime.now().strftime("%m ") + '月' + datetime.now().strftime(" %d")

    class_info = ""

    # 获取用户群信息
    if 'group_id' in session.ctx.keys():
        group_id = session.ctx['group_id']
    else:
        group_id = await get_user_group(session.ctx['user_id'])

    classes = await data_source.get_today_class_info(group_id)
    group_name = ""
    for c in classes:
        class_info += message.morningcall_class_msg.format(
            class_num=c['class_num'],
            class_name=c['class_name']
        )

    love_days = (datetime.now() - datetime(year=2018,month=12,day=13)).days

    msg = message.morningcall_love_msg.format(
        **{'date': date,
           'weekday': weekday[datetime.now().weekday()],
           'main_weather': weather['cond_d'],
           'main_pos': DEFAULT_CITY,
           'pos1': CITY_HOME1,
           'pos2': CITY_HOME2,
           'tmp_max': weather['tmp_max'],
           'tmp_min': weather['tmp_min'],
           'weather1': weather1['cond_d'],
           'tmp_max1': weather1['tmp_max'],
           'tmp_min1': weather1['tmp_min'],
           'weather2': weather2['cond_d'],
           'tmp_max2': weather1['tmp_max'],
           'tmp_min2': weather2['tmp_min'],
           'class': class_info,
           'comf': weather['comf'],
           'uv': weather['uv'],
           'one': one,
           'love_days': love_days,
           'love_msg': render_expression(message.love_msg),
           })
    await session.send(msg)
