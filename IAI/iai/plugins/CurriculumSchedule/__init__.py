from none import on_command, command
from none import session, CommandSession
from .data_source import getClassInfo
import time


@on_command('kcb', aliases=('课程表','课程'))
async def CurriculumSchedule(session: CommandSession):
    localtime = time.localtime(time.time())
    result = "课程信息"
    if 'week' not in session.args.keys() and\
            'weekday' not in session.args.keys()and\
            'classnum' not in session.args.keys()and\
            'next_class' not in session.args.keys():
        session.get('classnum',prompt='你要查询今天的第几节课？')

    if 'weekday' not in session.args.keys():
        session.args['weekday'] = localtime.tm_wday
    if 'week' not in session.args.keys():
        session.args['week'] = time.strftime("%W")

    if 'next_class' in session.args.keys():
        session.args['classnum'] = GetNextClassNum()

    result += await ClassesInfo(session.args["week"],session.args["weekday"],session.args["classnum"])
    await session.send(result)

@CurriculumSchedule.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.current_key:
        session.args[session.current_key] = stripped_arg

def GetNextClassNum():
    # Todo 实现获取下节课的序号
    return 4


async def ClassesInfo(week,weekday,classnum = None,nextclass = False):

    result = f'''
    要获取第 {week} 周
    星期 {weekday+1}
    第 {classnum} 节课的课表
    '''
    if classnum:
        result = await ClassInfo(week,weekday,classnum)

    else:
        for i in range(5):
            result += await ClassInfo(week, weekday, i+1)

    return str(result)

async def ClassInfo(week,weekday,classnum = None,nextclass = False):

    info = getClassInfo(week, weekday, classnum)
    result = f'''
☘️
第 {classnum} 节
【{info['subject']}】
👉 地点： {info['place']}
☕   教师：{info['teacher']}
    '''.strip()
    return str(result)

