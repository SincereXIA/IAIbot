from none import on_command, command,on_natural_language, NLPSession, NLPResult
from none import session, CommandSession,get_bot
from .data_source import getClassInfo, getRecentClassInfo,get_session_week
from datetime import datetime
from IAI.setup import *
from IAI.nlp.curriculum_nlp import curriculum_nlp
from IAI.iai.plugins.DoYouKnow import do_you_know

@on_command('kcb', aliases=('课程表', '课程'), only_to_me=False)
async def CurriculumSchedule(session: CommandSession):
    localtime = datetime.now()
    result = "课程信息"
    if 'week' not in session.args.keys() and \
            'weekday' not in session.args.keys() and \
            'classnum' not in session.args.keys() and \
            'next_class' not in session.args.keys():
        session.get('classnum', prompt='你要查询今天的第几节课？')

    if 'weekday' not in session.args.keys():
        session.args['weekday'] = localtime.weekday()
    if 'week' not in session.args.keys():
        await get_session_week(localtime)

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


async def ClassInfo(week, weekday, group_id, classnums = None,from_schedule = False, next_class=False):
    if classnums is None:
        classnums = [1,2,3,4,5]
    if next_class:
        if from_schedule:
            infos = await getRecentClassInfo(datetime.now(), group_id, timeLimit=30)
        else:
            infos = await getRecentClassInfo(datetime.now(), group_id,)
    else:
        infos = getClassInfo(week, weekday, group_id, classnums)
    result = ''
    class_num = ['1-2', '3-4', '5-6', '7-8', '9-10']
    if infos :
        for info in infos:
            result += f'''
┌───    {info.group_name}
│    第 {class_num[info.class_num-1]} 节
│    【{info.class_name}】
│    地点： {info.place}
│    教师：{info.teacher}
│    时间：{info.start_time.strftime('%H:%M')}
        '''
    else:
        result += "没有找到有关的课程信息哦"

    if get_bot().config.OPEN_DO_YOU_KNOW:
        result += f'''
--------
{await do_you_know()}'''
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
