from none import on_command, CommandSession
from datetime import datetime
from . import message
from . import data_source

@on_command('出')
async def user_add_item(session:CommandSession):
    item_name = session.get('item_name',prompt=message.add_item.item_name_msg)
    item_info = session.get('item_info',prompt=message.add_item.item_info_msg.format(item_name = item_name))
    seller_id = session.ctx['user_id']
    if 'group_id' in session.ctx.keys():
        from_group_id = session.ctx['group_id']
    else:
        from_group_id = None
    localtime = datetime.now()
    cfm =  session.get('cfm',prompt=message.add_item.item_add_confirm.format(
        item_name = item_name,
        item_info = item_info,
        seller_id = seller_id
    ))
    if cfm is 'y':
        await data_source.add_item(**session.args, seller_id=seller_id, from_group_id=from_group_id)
        await session.send('物品信息发布成功')

@user_add_item.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.current_key:
        session.args[session.current_key] = stripped_arg

@on_command('收')
async def user_find_item(session:CommandSession):
    key_word = session.get('key_word',prompt=message.find_item.item_name_msg)
    msg = await print_item_list(key_word)
    await session.send(msg)

@user_find_item.args_parser
async def _(session:CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.current_key:
        session.args[session.current_key] = [stripped_arg]

async def print_item_list(key_words):
    """
    生成可供打印的物品信息
    :param key_words:
    :return:
    """
    items = await data_source.get_item_list(key_words)
    msg = ''''''
    for item in items:
        msg+= message.find_item.item_msg.format(id = item.id, item_name = item.item_name,
                                                item_info = item.item_info)
    return msg

async def print_item_info(id):
    item = await data_source.get_item(id)
    msg = message.find_item.item_detail.format(id = item.id, item_name = item.item_name,
                                               item_info = item.item_info, seller_id = item.seller_id)
    return msg

