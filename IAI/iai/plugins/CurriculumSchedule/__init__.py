from none import on_command, command
from none import session, CommandSession
from .data_source import getClassInfo
from datetime import datetime
from IAI.setup import *


@on_command('kcb', aliases=('课程表','课程'))
async def CurriculumSchedule(session: CommandSession):
    localtime = datetime.now()
    curriculumStart = datetime(2018,9,3)
    result = "课程信息"
    if 'week' not in session.args.keys() and\
            'weekday' not in session.args.keys()and\
            'classnum' not in session.args.keys()and\
            'next_class' not in session.args.keys():
        session.get('classnum',prompt='你要查询今天的第几节课？')

    if 'weekday' not in session.args.keys():
        session.args['weekday'] = localtime.weekday()
    if 'week' not in session.args.keys():
        session.args['week'] = (int(localtime.strftime("%j"))-int(localtime.strftime("%j")))%7

    if 'next_class' in session.args.keys():
        session.args['classnum'] = GetNextClassNum()
    if 'group_id' not in session.ctx.keys():
        group_id = DEFAULT_GROUP
    else:
        group_id = session.ctx['group_id']


    result += await ClassesInfo(session.args["week"],session.args["weekday"],group_id,session.args["classnum"])
    await session.send(result)

@CurriculumSchedule.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.current_key:
        session.args[session.current_key] = stripped_arg

def GetNextClassNum():
    # Todo 实现获取下节课的序号
    return 4


async def ClassesInfo(week,weekday,group_id, classnum = None,):

    result = f'''
    要获取第 {week} 周
    星期 {weekday+1}
    第 {classnum} 节课的课表
    '''
    if classnum:
        result += await ClassInfo(week,weekday,group_id,classnum)

    else:
        for i in range(5):
            result += await ClassInfo(week, weekday, i+1)

    return str(result)

async def ClassInfo(week,weekday,group_id,classnum):

    info = getClassInfo(week, weekday, group_id,classnum)
    result = f'''
☘️
第 {classnum} 节
【{info.class_name}】
👉 地点： {info.place}
☕   教师：{info.teacher}
    '''.strip()
    return str(result)

