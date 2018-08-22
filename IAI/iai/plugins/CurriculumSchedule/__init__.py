from none import on_command, command
from none import session, CommandSession
from .data_source import getClassInfo,getRecentClassInfo
from datetime import datetime
from IAI.setup import *


@on_command('kcb', aliases=('课程表','课程'))
async def CurriculumSchedule(session: CommandSession):
    localtime = datetime.now()
    curriculumStart = datetime(2018,9,3) # todo 自定义设置
    result = "课程信息"
    if 'week' not in session.args.keys() and\
            'weekday' not in session.args.keys()and\
            'classnum' not in session.args.keys()and\
            'next_class' not in session.args.keys():
        session.get('classnum',prompt='你要查询今天的第几节课？')

    if 'weekday' not in session.args.keys():
        session.args['weekday'] = localtime.weekday()
    if 'week' not in session.args.keys():
        day = int(localtime.strftime("%j"))-int(curriculumStart.strftime("%j"))
        if day >= 0:
            session.args['week'] = day%7
        else:
            session.args['week'] = day%-7

    next_class = False
    if 'next_class' in session.args.keys():
        next_class = True
    if 'group_id' not in session.ctx.keys():
        group_id = DEFAULT_GROUP
    else:
        group_id = session.ctx['group_id']


    result += await ClassesInfo(**session.args, group_id = group_id)
    await session.send(result)

@CurriculumSchedule.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.current_key:
        session.args[session.current_key] = stripped_arg
    elif '下一' in stripped_arg or '下节' in stripped_arg:
        session.args['next_class'] = True


def GetNextClassNum():
    # Todo 实现获取下节课的序号
    return 4


async def ClassesInfo(week,weekday,group_id, classnum = None, next_class = False):

    result = f'''
    要获取第 {week} 周
    星期 {weekday+1}
    第 {classnum} 节课的课表
    '''
    if next_class:
        result += await ClassInfo(week,weekday,group_id,classnum,next_class)
    elif classnum:
        result += await ClassInfo(week,weekday,group_id,classnum)
    else:
        for i in range(5):
            result += await ClassInfo(week, weekday, i+1,classnum)

    return str(result)

async def ClassInfo(week,weekday,group_id,classnum,next_class = False):

    if next_class:
        info = getRecentClassInfo(datetime.now(),group_id)
    else:
        info = getClassInfo(week, weekday, group_id,classnum)
    result = f'''
☘️
第 {classnum} 节
【{info.class_name}】
👉 地点： {info.place}
☕   教师：{info.teacher}
    '''.strip()
    return str(result)

