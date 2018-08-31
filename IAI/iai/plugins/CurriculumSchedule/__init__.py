from none import on_command,on_natural_language, NLPSession, NLPResult
from none import CommandSession,get_bot
from .data_source import getClassInfo, getRecentClassInfo,get_session_week
from datetime import datetime
from IAI.setup import *
from IAI.nlp.curriculum_nlp import curriculum_nlp
from IAI.iai.plugins.DoYouKnow import do_you_know
from IAI.iai.common.QQUser import get_user_group

@on_command('kcb', aliases=('课程表', '课程'), only_to_me=False)
async def CurriculumSchedule(session: CommandSession):
    localtime = datetime.now()
    if 'from_schedule' in session.args.keys():
        result = "☕ 以下课程即将开始上课：\n"
    else:
        result = "课程信息：\n"
    if 'week' not in session.args.keys() and \
            'weekday' not in session.args.keys() and \
            'classnums' not in session.args.keys() and \
            'next_class' not in session.args.keys():
        session.get('classnums', prompt='你要查询今天的第几节课？')

    if 'weekday' not in session.args.keys():
        session.args['weekday'] = localtime.weekday()
    if 'week' not in session.args.keys():
        session.args['week'] = get_session_week(localtime)

    if 'group_id' not in session.ctx.keys():
        group_id = await get_user_group(session.ctx['user_id'])
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


async def ClassInfo(week, weekday, group_id, classnums = None,from_schedule = False, next_class=False, **kw):
    if classnums is None:
        classnums = [1,2,3,4,5]
    elif not isinstance(classnums,list):
        classnums = list(classnums)
    if next_class:
        if from_schedule:
            infos = await getRecentClassInfo(datetime.now(), group_id, timeLimit=30)
        else:
            infos = await getRecentClassInfo(datetime.now(), group_id,)
    else:
        infos = getClassInfo(week, weekday, group_id, classnums)
    result = f'第 {week} 教学周  星期{weekday+1}'
    class_num = ['1-2', '3-4', '5-6', '7-8', '9-10']
    group_name = ""
    if infos :
        for info in infos:
            if info.group_name != group_name and group_name != "":
                result += f'''
└───  '''
            if info.group_name != group_name:
                group_name = info.group_name
                result += f'''
┌───    {info.group_name}'''
            result+=f'''
│    ☛ 第 {class_num[info.class_num-1]} 节
│    【{info.class_name}】
│    地点： {info.place}
│    教师：{info.teacher}
│    时间：{info.start_time.strftime('%H:%M')}'''
        else:
            result += f'''
└───'''
    else:
        result += "没有找到有关的课程信息哦"

    if get_bot().config.OPEN_DO_YOU_KNOW and from_schedule:
        result += f'''        
{await do_you_know()}'''
    return str(result)

@on_natural_language({'课'},only_to_me= False, only_short_message=True)
async def _(session: NLPSession):
    args = await curriculum_nlp(session.msg_text)
    #await session.send(f'''NLP DEBUG_INFO:{args['debug_info']}+  SCORE:{args['score']}''')
    if args['score']>= 0.66:
        args.pop('debug_info')
        args.pop('score')
        return NLPResult(90,'kcb',args)
    else:
        return None
