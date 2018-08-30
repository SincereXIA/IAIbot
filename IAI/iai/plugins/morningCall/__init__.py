import none
from none import session, CommandSession, on_command, get_bot
from . import data_source, message
from IAI.iai.plugins.weather.data_source import get_today_weather_info
from datetime import datetime
from IAI.iai.common.QQUser import get_user_group


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
        if c['group_name'] != group_name:
            group_name = c['group_name']
            class_info += f'\n---\n{group_name}'
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
    data = await data_source.get_one_content()
    msg = f'''
    {data['text']}
    —— {data['info']}
    '''
    await session.send(msg)


async def one_msg():
    data = await data_source.get_one_content()
    msg = f'''
    「{data['text']}」
    —— {data['info']}
        '''
    return msg
