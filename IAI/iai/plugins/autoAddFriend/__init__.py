from none import on_request,RequestSession,get_bot,on_notice,NoticeSession,\
    on_command, CommandSession
import time
import random
import requests,json
from . import data_source
from IAI.iai.common import GroupInfo

@on_request('friend')
async def _(session: RequestSession):
    time.sleep(random.randrange(2,5))
    await session.approve()
    return

@on_notice('group_increase')
async def _(session: NoticeSession):
    bot = get_bot()
    time.sleep(random.randrange(2, 5))
    url = f'http://{bot.config.IP_ADDRESS}:{bot.config.IP_PORT}/get_group_member_list'
    rs = requests.get(url, {'group_id': session.ctx['group_id']})
    r = json.loads(rs.text)

    count = [0,0]
    for i in r['data']:
        i['qq_id'] = i['user_id']
        i['group_card'] = i['card']
        i['group_role'] = i['role']
        count[await data_source.add_QQUser(**i)] += 1
    msg = f'''
初始化群成员信息成功，
新增了 {count[0]} 个成员信息，
更新了 {count[1]} 个成员信息。
    '''

    try:
        url = f'http://{bot.config.IP_ADDRESS}:{bot.config.IP_PORT}/_get_group_info'
        rs = requests.get(url, {'group_id': session.ctx['group_id']})
        r = json.loads(rs.text)
        group_name = r['data']['group_name']
    except Exception:
        group_name = None
    try:
        await GroupInfo.add_group_info(group_id=session.ctx['group_id'],group_name=group_name)
        msg += '\n群信息已添加至计划任务\n'
    except Exception:
        pass

    ctx = {'message_type': 'group', 'self_id': get_bot().config.ROBOT_ID, 'group_id': session.ctx['group_id']}
    await get_bot().send(ctx,msg)

@on_request('group')
async def _(session:RequestSession):
    time.sleep(random.randrange(2, 5))
    await session.approve()

@on_command('group_refresh')
async def group_refresh(session:CommandSession):
    bot = get_bot()
    time.sleep(random.randrange(2, 5))
    url = f'http://{bot.config.IP_ADDRESS}:{bot.config.IP_PORT}/get_group_member_list'
    rs = requests.get(url, {'group_id': session.ctx['group_id']})
    r = json.loads(rs.text)

    count = [0, 0]
    for i in r['data']:
        i['qq_id'] = i['user_id']
        i['group_card'] = i['card']
        i['group_role'] = i['role']
        count[await data_source.add_QQUser(**i)] += 1
    msg = f'''
    刷新群成员信息成功，
    新增了 {count[0]} 个成员信息，
    更新了 {count[1]} 个成员信息。
        '''
    try:
        url = f'http://{bot.config.IP_ADDRESS}:{bot.config.IP_PORT}/_get_group_info'
        rs = requests.get(url, {'group_id': session.ctx['group_id']})
        r = json.loads(rs.text)
        group_name = r['data']['group_name']
    except Exception:
        group_name = None
    try:
        await GroupInfo.add_group_info(group_id=session.ctx['group_id'],group_name=group_name)
        msg += '\n群信息已添加至计划任务\n'
    except Exception:
        pass
    ctx = {'message_type': 'group', 'self_id': get_bot().config.ROBOT_ID, 'group_id': session.ctx['group_id']}
    await get_bot().send(ctx, msg)