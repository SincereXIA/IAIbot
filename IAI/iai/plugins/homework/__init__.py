from none import on_command, CommandSession, get_bot
from IAI.iai.plugins.homework.data_source import get_homework_info, Homework, add_homework_info
from datetime import date
from IAI.nlp.datetime_nlp import date_nlp


@on_command('homework', aliases=('作业是啥','今日作业'), only_to_me= False)
async def homework(session: CommandSession):
    bot = get_bot()
    if 'group_id' not in session.ctx.keys():
        group_id = bot.config.DEFAULT_GROUP
    else:
        group_id = session.ctx['group_id']

    localdate = date.today()
    await session.send(await homework_info(group_id, localdate))


@on_command('add_homework', aliases=('布置作业', '添加作业'))
async def add_homework(session: CommandSession):
    bot = get_bot()
    if 'group_id' not in session.ctx.keys():
        group_id = bot.config.DEFAULT_GROUP
    else:
        group_id = session.ctx['group_id']

    subject_name = session.get('subject_name', prompt='请输入课程科目')
    content = session.get('content', prompt='请输入作业内容')
    end_date = session.get('content', prompt='作业什么时候收？')
    end_date = await date_nlp(end_date)
    assign_for = session.get('assign_for', prompt='收哪些人的？')
    add_date = date.today()

    homework_message = f'''
科目:\t{subject_name}
作业:\t{content}
DDL:\t{end_date}

----
以上信息确认无误吗？
添加到数据库请回复: 'y'
添加并即刻推送请回复: 't'
删除此作业请回复: 'n'
    '''
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


async def homework_info(group_id, localdate: date) -> str:
    result = f'''
{localdate.month} 月 {localdate.day} 日的作业信息'''
    homeworks = await get_homework_info(group_id, localdate)
    for homework in homeworks:
        result += f'''
科目：{homework.subject_name}
作业：{homework.content}
        '''

    return str(result)
