import re

from none import on_command, CommandSession, get_bot, NLPResult
from datetime import datetime
from . import message
from . import data_source
from . import nlp
import none


@on_command('add_item', aliases="出")
async def user_add_item(session: CommandSession):
    item_name = session.get('item_name', prompt=message.add_item.item_name_msg)
    session.get('item_info', prompt=message.add_item.item_info_msg.format(item_name=item_name))
    if session.current_arg_images:
        for image in session.current_arg_images:
            session.args['item_info'] += f'''
{image}
                '''
    seller_id = session.ctx['user_id']
    if 'group_id' in session.ctx.keys():
        from_group_id = session.ctx['group_id']
    else:
        from_group_id = None
    localtime = datetime.now()
    cfm = session.get('cfm', prompt=message.add_item.item_add_confirm.format(
        item_name=item_name,
        item_info=session.args['item_info'],
        seller_id=seller_id
    ))
    if cfm is 'y':
        await data_source.add_item(**session.args, seller_id=seller_id, from_group_id=from_group_id)
        await session.send('物品信息发布成功')
    else:
        await session.send('操作已取消')


@user_add_item.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg == 'q':
        await session.send("退出本次会话")
        session.finish()
    if session.current_key:
        session.args[session.current_key] = stripped_arg
    elif stripped_arg:
        session.args['item_name'] = stripped_arg


@on_command('find_item', aliases=("查",))
async def user_find_item(session: CommandSession):
    key_word = session.get('key_word', prompt=message.find_item.item_name_msg)
    if '全部' in key_word or '所有' in key_word:
        key_word = None
    if 'page' not in session.args.keys():
        session.args['page'] = 1

    if 'type' not in session.args.keys():
        session.args['type'] = "sell"
    if not 'continue' in session.args.keys():
        msg = await print_item_list_from_keys(key_word, session.args['page'], session.args['type'])
        await session.send(msg + message.find_item.item_list_msg)
    while True:
        cmd = session.get('cmd')
        if '下一页' in cmd or 'n' in cmd:
            session.args['page'] += 1
            session.args.pop('cmd')
            try:
                session.args.pop('continue')
            except Exception:
                pass
            await user_find_item(session)
            return
        elif '上一页' in cmd or 'n' in cmd:
            session.args['page'] -= 1
            session.args.pop('cmd')
            try:
                session.args.pop('continue')
            except Exception:
                pass
            await user_find_item(session)
            return
        else:
            try:
                id = int(cmd[0])
            except Exception:
                await session.send("输入有误，退出本次检索")
                session.finish()
                return
            await session.send(await print_item_info(id)+message.find_item.item_detail_more)
            session.args.pop('cmd')
            session.args['continue'] = True


@user_find_item.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg == 'q':
        await session.send("退出本次会话")
        session.finish()
    if session.current_key:
        session.args[session.current_key] = stripped_arg.split(" ")
    elif stripped_arg:
        split_arg = stripped_arg.split(" ")
        session.args['key_word'] = split_arg
        if '收' in split_arg:
            session.args['type'] = "want"
            session.args['key_word'].remove("收")


async def print_item_list_from_keys(key_words, page=1, type="sell", ):
    """
    生成可供打印的物品信息
    :param key_words:
    :return:
    """
    msg = ''
    if key_words:
        msg += f'''
关于 {key_words} 找到以下内容：
        '''
    items = await data_source.get_item_list(key_words, type)
    if page > len(items) // 10 + 1:
        return "当前已经是最后一页了哦"
    if type == 'sell':
        msg += "有人想出这些东西：\n"
    else:
        msg += "有人想要这些东西：\n"
    msg += f'''第{page}页，共{len(items)//10+1}页'''
    start = (page - 1) * 10
    if start + 10 > len(items):
        end = len(items)
    else:
        end = start + 10

    for item in items[start:end]:
        if len(item.item_name) > 15:
            item_name = item.item_name[:15]
        else:
            item_name = item.item_name
        item_info = replace_all_url(item.item_info)
        msg += message.find_item.item_msg.format(id=item.id, item_name=item_name,
                                                 item_info=item_info)
    return msg


async def print_item_list(items, page=1):
    if page < 1 :
        return "当前已经是第一页了哦"
    if page > len(items) // 10 + 1:
        return "当前已经是最后一页了哦"
    msg = f'''第{page}页，共{len(items)//10+1}页'''
    start = (page - 1) * 10
    if start + 10 > len(items):
        end = len(items)
    else:
        end = start + 10

    for item in items[start:end]:
        if len(item.item_name) > 15:
            item_name = item.item_name[:15]
        else:
            item_name = item.item_name
        item_info = replace_all_url(item.item_info)
        msg += message.find_item.item_msg.format(id=item.id, item_name=item_name,
                                                 item_info=item_info)
    return msg


async def print_item_info(id, is_seller=False):
    item = await data_source.get_item(id)
    msg = message.find_item.item_detail.format(id=item.id, item_name=item.item_name,
                                               item_info=item.item_info, seller_id=item.seller_id,
                                               add_time=item.add_time)
    return msg


def replace_all_url(sentence):
    r = re.compile(
        r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))')
    url_list = r.findall(sentence)
    for j in url_list:
        # sentence = sentence.replace(j[0], '<URL>')
        sentence = sentence.replace(j[0], '[图片]')
    return sentence


@on_command('user_items', aliases=("我的",))
async def user_items(session: CommandSession):
    seller_id = session.ctx['user_id']
    items = await data_source.get_my_item(seller_id)
    msg = await print_item_list(items)
    if not 'continue' in session.args.keys():
        await session.send(msg + message.find_item.item_list_msg)
        session.args['continue'] = True
    while True:
        cmd = session.get('cmd')
        if '下一页' in cmd or 'n' in cmd:
            session.args['page'] += 1
            session.args.pop('cmd')
            try:
                session.args.pop('continue')
            except Exception:
                pass
            await user_find_item(session)
            return
        elif '上一页' in cmd or 'n' in cmd:
            session.args['page'] -= 1
            session.args.pop('cmd')
            try:
                session.args.pop('continue')
            except Exception:
                pass
            await user_find_item(session)
            return
        else:
            try:
                id = int(cmd[0])
            except Exception:
                await session.send("退出本次检索")
                session.finish()
                return
            await session.send(await print_item_info(id))
            session.args.pop('cmd')
            session.args['continue'] = True


@user_items.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg == 'q':
        await session.send("退出本次会话")
        session.finish()
    if session.current_key:
        session.args[session.current_key] = stripped_arg.split(" ")

    elif stripped_arg:
        split_arg = stripped_arg.split(" ")
        session.args['key_word'] = split_arg
        if '收' in split_arg:
            session.args['type'] = "want"
            session.args['key_word'].remove("收")



@on_command('want_item', aliases="收")
async def user_want_item(session: CommandSession):
    item_name = session.get('item_name', prompt=message.want_item.item_name_msg)
    session.get('item_info', prompt=message.want_item.item_info_msg.format(item_name=item_name))
    if session.current_arg_images:
        for image in session.current_arg_images:
            session.args['item_info'] += f'''
{image}
                '''
    seller_id = session.ctx['user_id']
    if 'group_id' in session.ctx.keys():
        from_group_id = session.ctx['group_id']
    else:
        from_group_id = None
    localtime = datetime.now()
    cfm = session.get('cfm', prompt=message.want_item.item_add_confirm.format(
        item_name=item_name,
        item_info=session.args['item_info'],
        seller_id=seller_id
    ))
    if cfm is 'y':
        await data_source.add_item(**session.args, type="want", seller_id=seller_id, from_group_id=from_group_id)
        await session.send('收购信息发布成功')


@user_want_item.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg == 'q':
        await session.send("退出本次会话")
        session.finish()
    if session.current_key:
        session.args[session.current_key] = stripped_arg
    elif stripped_arg:
        session.args['item_name'] = stripped_arg


@on_command('del_item', aliases="删")
async def del_item(session: CommandSession):
    id = session.get('id', prompt="请输入要删除的条目编号:")
    try:
        id = int(id)
    except Exception:
        await session.send('条目编号有误')
        session.finish()
        return
    item = await data_source.get_item(id)
    if str(item.seller_id) != str(session.ctx['user_id']) and \
            session.ctx['user_id'] not in get_bot().config.sell_admins:
        await session.send('你没有权限变动此条目')
        session.finish()
        return
    else:
        msg = '''
你确定要删除此信息？
        '''
        msg += await print_item_info(id)
        msg += message.user_center.del_confirm_msg
        cmd = session.get('cmd', prompt=msg)
        if cmd == 'y':
            await data_source.del_item(id)
            await session.send(f"删除条目{id}成功")
        else:
            await session.send("本次操作取消")


@del_item.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg == 'q':
        await session.send("退出本次会话")
        session.finish()
    if session.current_key:
        session.args[session.current_key] = stripped_arg
    elif stripped_arg:
        session.args['id'] = stripped_arg


@on_command('update_item', aliases="改")
async def update_item(session: CommandSession):
    id = session.get('id', prompt="请输入要修改的条目编号:")
    try:
        id = int(id)
    except Exception:
        await session.send('条目编号有误')
        session.finish()
        return
    item = await data_source.get_item(id)
    if str(item.seller_id) != str(session.ctx['user_id']) and \
            session.ctx['user_id'] not in get_bot().config.sell_admins:
        await session.send('你没有权限变动此条目')
        session.finish()
        return
    else:
        msg = message.user_center.update_item_name_msg.format(item_name=item.item_name)
        item_name = session.get('item_name', prompt=msg)
        if item_name == 'n':
            item_name = None
        msg = message.user_center.update_item_info_msg.format(item_info=item.item_info)
        item_info = session.get('item_info', prompt=msg)
        if item_info == 'n':
            item_info = None
        await data_source.update_item(id, item_name, item_info)
        await session.send("信息修改成功！")

@update_item.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg == 'q':
        await session.send("退出本次会话")
        session.finish()
    if session.current_key:
        session.args[session.current_key] = stripped_arg
    elif stripped_arg:
        session.args['id'] = stripped_arg
