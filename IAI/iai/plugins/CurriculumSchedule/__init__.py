from none import on_command, command,on_natural_language, NLPSession, NLPResult
from none import session, CommandSession,get_bot
from .data_source import getClassInfo, getRecentClassInfo,get_session_week
from datetime import datetime
from IAI.setup import *
from IAI.nlp.curriculum_nlp import curriculum_nlp


@on_command('kcb', aliases=('课程表', '课程'), only_to_me=False)
async def CurriculumSchedule(session: CommandSession):
    localtime = datetime.now()
    curriculumStart = datetime(2018, 9, 3)  # todo 自定义设置
    result = "课程信息"
    if 'week' not in session.args.keys() and \
            'weekday' not in session.args.keys() and \
            'classnum' not in session.args.keys() and \
            'next_class' not in session.args.keys():
        session.get('classnum', prompt='你要查询今天的第几节课？')

    if 'weekday' not in session.args.keys():
        session.args['weekday'] = localtime.weekday()
    if 'week' not in session.args.keys():
        get_session_week(localtime)

    if 'group_id' not in session.ctx.keys():
        group_id = DEFAULT_GROUP
    else:
        group_id = session.ctx['group_id']

    result += await ClassInfo(**session.args, group_id=group_id,)
    await session.send(result)


@CurriculumSchedule.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.current_key:
        session.args[session.current_key] = stripped_arg
    elif '下一' in stripped_arg or '下节' in stripped_arg:
        session.args['next_class'] = True



async def ClassesInfo(week, weekday, group_id, classnum=None, next_class=False):
    result = f'''
    要获取第 {week} 周
    星期 {weekday+1}
    第 {classnum} 节课的课表
    '''
    if next_class:
        result += await ClassInfo(week, weekday, group_id, classnum, next_class)
    elif type(classnum) == int:
        result += await ClassInfo(week, weekday, group_id, classnum)
    else:
        for i in range(5):
            result += await ClassInfo(week, weekday, i + 1, classnum)

    return str(result)


async def ClassInfo(week, weekday, group_id, classnums = None, next_class=False):
    if classnums is None:
        classnums = [1,2,3,4,5]
    if next_class:
        infos = getRecentClassInfo(datetime.now(), group_id, timeLimit=20)
    else:
        infos = getClassInfo(week, weekday, group_id, classnums)
    result = ''
    if infos :
        for info in infos:
            result += f'''
┌────
│    第 {info.class_num} 节
│    【{info.class_name}】
│    地点： {info.place}
│    教师：{info.teacher}
│    时间：{info.start_time.strftime('%H:%M')}
        '''
    else:
        result += "没有找到有关的课程信息哦"
    return str(result)

@on_natural_language({'课'},only_to_me= False, only_short_message=True)
async def _(session: NLPSession):
    args = await curriculum_nlp(session.msg_text)
    #await session.send(f'''NLP DEBUG_INFO:{args['debug_info']}+  SCORE:{args['score']}''')
    if args['score']>= 0.7:
        args.pop('debug_info')
        args.pop('score')
        return NLPResult(90,'kcb',args)
    else:
        return None
