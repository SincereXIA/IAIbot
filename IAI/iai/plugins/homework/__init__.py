from none import on_command, CommandSession, get_bot, on_natural_language, NLPSession, NLPResult
from IAI.iai.plugins.homework.data_source import get_homework_info, Homework, add_homework_info
from datetime import date,datetime
from IAI.nlp.datetime_nlp import date_nlp
from IAI.nlp.homework_nlp import get_subject_name
import IAI.iai.plugins.homework.message as bot_message
from IAI.iai.common.QQUser import get_user_group, get_user
import time


@on_command('homework', aliases=('作业是啥', '今日作业'), only_to_me=False)
async def homework(session: CommandSession):
    try:
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
    except Exception as e:
        await session.send('糟糕，运行出错了，错误信息：' + str(e))


@on_command('add_homework', aliases=('布置作业', '添加作业'))
async def add_homework(session: CommandSession):
    try:
        if 'group_id' not in session.ctx.keys():
            group_id = await get_user_group(session.ctx['user_id'])
        else:
            group_id = session.ctx['group_id']

        subject_name = session.get('subject_name', prompt=bot_message.add_homework_msg.subject_name_msg)
        content = session.get('content', prompt=bot_message.add_homework_msg.get_content)
        if session.current_arg_images:
            for image in session.current_arg_images:
                session.args['content'] += f'''
{image}
                '''
        end_date = session.get('end_date', prompt=bot_message.add_homework_msg.end_date_msg)
        end_date = await date_nlp(end_date)
        if end_date < datetime.now():
            await session.send('你不能添加一个 DDL 小于今日的作业，请重新输入截止日期')
            session.args.pop('end_date')
            time.sleep(1)
            session.pause()

        assign_for = session.get('assign_for', prompt=bot_message.add_homework_msg.assign_for_msg)
        add_date = date.today()

        end_date_msg = end_date.strftime("%m ") + '月' + end_date.strftime(" %d") + ' 日，星期' + \
                       ['一', '二', '三', '四', '五', '六', '日'][end_date.weekday()]
        homework_message = bot_message.add_homework_msg.confirm.format(
            subject_name=subject_name,
            content=content,
            end_date=end_date_msg,
            assign_for=assign_for
        )

        # 获取用户信息
        user = await get_user(session.ctx['user_id'])
        if user:
            add_by = user.nickname
        else:
            add_by = session.ctx['user_id']

        instruction = session.get('instruction', prompt=homework_message)

        if instruction is 'y' or instruction is 't':
            # 写入数据库
            homework = await add_homework_info(group_id=group_id, subject_name=subject_name,
                                               content=content, end_date=end_date,
                                               assign_for=assign_for, add_by=add_by,
                                               added_date=add_date
                                               )
            await session.send('作业信息添加完成')
            if instruction is 't':
                time.sleep(2)
                await push_homework(homework, group_id)
        else:
            await session.send('操作已取消')
    except Exception as e:
        await session.send('出现错误了，错误信息：'+str(e))


@add_homework.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.current_key:
        session.args[session.current_key] = stripped_arg


async def homework_info(group_id, localdate: date, subjects=None) -> str:
    """
    根据群号码，日期，获取可供打印的作业信息
    :param group_id: 群号码
    :param localdate: 日期
    :param subjects: 科目
    :return: str
    """
    if subjects:
        result = bot_message.get_homework_msg.subject_homework_msg.format(subject=str(subjects))
    else:
        result = f'''
{localdate.month} 月 {localdate.day} 日的作业信息如下'''

    homeworks = await get_homework_info(group_id, localdate, subjects)
    if not homeworks:
        result += bot_message.get_homework_msg.no_homework_msg
    else:
        result += print_homework_info(homeworks)
    return str(result)


@on_natural_language('作业', only_to_me=False, only_short_message=True)
async def _(session: NLPSession):
    rs = get_subject_name(session.msg_text)
    if rs['score'] > 0.65:
        return NLPResult(90, 'homework', {'subjects': rs['subjects']})


def print_homework_info(homeworks):
    """
    获取可供打印的作业信息
    :param homeworks: 列表形式的作业数据库信息
    :return: str
    """
    result = ""
    for homework in homeworks:
        end_date_msg = str(homework.end_date.month) + '月' + str(homework.end_date.day) + ' 日，星期' + \
                       ['一', '二', '三', '四', '五', '六', '日'][homework.end_date.weekday()]
        result += bot_message.get_homework_msg.homework_msg.format(
            subject_name=homework.subject_name,
            content=homework.content,
            end_date=end_date_msg,
            assign_for=homework.assign_for
        )
    return result


async def push_homework(homework, group_id):
    """
    推送作业信息至群聊
    :param homework:
    :return:
    """
    msg = "【推送】作业信息：\n"
    msg += print_homework_info([homework])
    ctx = {'message_type': 'group', 'self_id': get_bot().config.ROBOT_ID, 'group_id': int(group_id)}
    await get_bot().send(ctx, msg)
