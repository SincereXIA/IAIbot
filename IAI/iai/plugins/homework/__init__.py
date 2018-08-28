from none import on_command, CommandSession, get_bot, on_natural_language, NLPSession, NLPResult
from IAI.iai.plugins.homework.data_source import get_homework_info, Homework, add_homework_info
from datetime import date
from IAI.nlp.datetime_nlp import date_nlp
from IAI.nlp.homework_nlp import get_subject_name
import IAI.iai.plugins.homework.message as bot_message


@on_command('homework', aliases=('作业是啥','今日作业'), only_to_me= False)
async def homework(session: CommandSession):
    bot = get_bot()
    if 'group_id' not in session.ctx.keys():
        group_id = bot.config.DEFAULT_GROUP
    else:
        group_id = session.ctx['group_id']

    subjects = []
    if 'subjects' in session.args.keys():
        subjects = session.args['subjects']
    localdate = date.today()
    await session.send(await homework_info(group_id, localdate, subjects=subjects))


@on_command('add_homework', aliases=('布置作业', '添加作业'))
async def add_homework(session: CommandSession):
    bot = get_bot()
    if 'group_id' not in session.ctx.keys():
        group_id = bot.config.DEFAULT_GROUP
    else:
        group_id = session.ctx['group_id']

    subject_name = session.get('subject_name', prompt='请输入课程科目')
    content = session.get('content', prompt=bot_message.add_homework_msg.get_content)
    if session.current_arg_images:
        for image in session.current_arg_images:
            session.args['content']+=f'''
{image}
            '''
    end_date = session.get('end_date', prompt='作业什么时候收？')
    end_date = await date_nlp(end_date)
    assign_for = session.get('assign_for', prompt='收哪些人的？')
    add_date = date.today()

    homework_message = bot_message.add_homework_msg.confirm.format(
        subject_name=subject_name,
        content = content,
        end_date = end_date
    )
    instruction = session.get('instruction', prompt=homework_message)
    if instruction is 'y' or instruction is 't':
        await add_homework_info(group_id=group_id, subject_name=subject_name,
                                content=content, end_date=end_date,
                                assign_for=assign_for, add_by=session.ctx['user_id']
                                )
        await session.send('作业信息添加完成')
    else:
        await session.send('操作已取消')


@add_homework.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.current_key:
        session.args[session.current_key] = stripped_arg


async def homework_info(group_id, localdate: date, subjects = None) -> str:
    result = f'''
{localdate.month} 月 {localdate.day} 日的作业信息'''
    homeworks = await get_homework_info(group_id, localdate, subjects)
    for homework in homeworks:
        result += f'''
科目：{homework.subject_name}
作业：{homework.content}
DDL ：{homework.end_date} 
        '''

    return str(result)

@on_natural_language('作业', only_to_me= False)
async def _(session: NLPSession):
    rs = get_subject_name(session.msg_text)
    return NLPResult(90,'homework',{'subjects': rs['subjects']})

