from nonebot import on_command,CommandSession
from . import data_source,message

@on_command('del_homework', aliases=("删作业",))
async def del_homework(session: CommandSession):
    id = session.get('id', prompt="请输入要删除的作业编号:")
    try:
        id = int(id)
    except Exception:
        await session.send('条目编号有误')
        session.finish()
        return
    homework = await data_source.get_homework_info_by_id(id)

    try:
        assert str(session.ctx['group_id']) == str(homework.group_id)
    except Exception:
        await session.send('无权在非班群执行删除作业操作')
        return

    msg = '''
你确定要删除此作业？
    '''
    msg += message.del_homework_msg.confirm.format(subject_name = homework.subject_name,
                                                   content = homework.content,
                                                   assign_for = homework.assign_for,
                                                   end_date = homework.end_date)
    cmd = session.get('cmd', prompt=msg)
    if cmd == 'y':
        await data_source.del_homework(id)
        await session.send(f"删除条目{id}成功")
    else:
        await session.send("本次操作取消")

@del_homework.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg == 'q':
        await session.send("退出本次会话")
        session.finish()
    if session.current_key:
        session.args[session.current_key] = stripped_arg
    elif stripped_arg:
        session.args['id'] = stripped_arg