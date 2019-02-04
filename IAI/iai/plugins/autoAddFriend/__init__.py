from nonebot import on_request,RequestSession,get_bot,on_notice,NoticeSession,\
    on_command, CommandSession
import time
import random
import requests,json
from . import data_source,invite
from IAI.iai.common import GroupInfo,encodenum,decodenum

@on_request('friend')
async def _(session: RequestSession):
    #time.sleep(random.randrange(2,5))
    await invite.init_invite(session,call=False)
    await session.approve()
    bot = get_bot()
    try:
        url = f'http://{bot.config.IP_ADDRESS}:{bot.config.IP_PORT}/get_stranger_info'
        re = requests.get(url, {'user_id': session.ctx['user_id']})
        userinfo = json.loads(re.text)['data']
        if userinfo['sex'] == 'male':
            userinfo['sex'] = 1
        else:
            userinfo['sex'] = 2
        await data_source.add_QQUser(qq_id=str(userinfo['user_id']), nickname=userinfo['nickname'],
                                     sex=userinfo['sex'],group_role='friend')
    except Exception:
        pass

    msg = f'''真好呀，你没有错过我。
感谢相遇。祝好 ：）'''
    ctx = {'message_type': 'private', 'self_id': bot.config.ROBOT_ID, 'user_id': session.ctx['user_id']}
    await bot.send(ctx, msg)

    return

@on_notice('friend_add')
async def _(session: RequestSession):
    #time.sleep(random.randrange(2,5))
    await invite.init_invite(session,call=False)
    bot = get_bot()
    try:
        url = f'http://{bot.config.IP_ADDRESS}:{bot.config.IP_PORT}/get_stranger_info'
        re = requests.get(url, {'user_id': session.ctx['user_id']})
        userinfo = json.loads(re.text)['data']
        if userinfo['sex'] == 'male':
            userinfo['sex'] = 1
        else:
            userinfo['sex'] = 2
        await data_source.add_QQUser(qq_id=str(userinfo['user_id']), nickname=userinfo['nickname'],
                                     sex=userinfo['sex'],group_role='friend')
    except Exception:
        pass

    msg = f'''真好呀，你没有错过我。
感谢相遇。祝好 ：）'''
    await session.send(msg)

    return

@on_command('init_invite')
async def init_invite(session:CommandSession):
    await invite.init_invite(session)
    return

@on_notice('group_increase')
async def _(session: NoticeSession):
    bot = get_bot()
    time.sleep(random.randrange(2, 5))
    url = f'http://{bot.config.IP_ADDRESS}:{bot.config.IP_PORT}/get_group_member_list'
    rs = requests.get(url, {'group_id': session.ctx['group_id']})
    r = json.loads(rs.text)
    if int(session.ctx['user_id']) == int(bot.config.ROBOT_ID):
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
    else:
        msg = ""
        for i in r['data']:
            if int(i['user_id']) == int(session.ctx['user_id']):
                i['qq_id'] = i['user_id']
                i['group_card'] = i['card']
                i['group_role'] = i['role']
                await data_source.add_QQUser(**i)
                msg = f"欢迎新成员 {i['nickname']} 加入！"
                break

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


#@on_command('invite_from_user',aliases=('试吃','【内参试吃】','我要试吃'))
async def invite_from_user(session:CommandSession):
    qq_id = session.ctx['user_id']
    invite_by = session.get('invite_by',prompt=f'''
想参加免费泡芙的活动吗，非常简单噢！
只需要
1.回复“我要试吃”即可得到你的专属福利文案啦 
2.把福利转发给你的朋友们吧
3.邀请三个朋友加 内参君 为好友【并让Ta们把你的专属福利文案转发给内参君】~
4.恭喜你人气积攒成功，免费泡芙到手啦！
    ''')
    await invite.init_invite(session,call = False)
    try:
        invite_by = int(invite_by.strip())
        invite_by = await data_source.get_user_invite(invite_by)
        await data_source.invite_by(qq_id,invite_by.qq_id)
        msg = f"内参君知道 「{invite_by.nickname}」是你的好友啦，转发下面的专属福利文案给三个小伙伴，并让Ta们点击蓝色数字添加内参君为好友，把下面这条福利文案转发给内参君，你也能得到一张「香八度」美味泡芙免费卷 ~"

    except Exception:
        msg = '''欢迎参加西电内参君月饼试吃活动，转发下面的专属福利文案给三个小伙伴，并让Ta们点击蓝色数字添加内参君为好友，把这条福利文案转发给内参君，即可得到一张「香八度」美味泡芙免费卷哦'''

    await session.send(msg)
    await session.send(await invite_other(session.ctx['user_id']))

async def invite_other(qq_id):
    return f'''【内参试吃】  【福利口令】
来参加内参君的月饼节试吃活动吧

戳这里 ☛☛ 1739133243 
点击蓝色数字添加好友，加内参君为好友，来围观内参君空间的置顶说说~
【转发这条消息给内参君，还可获得『香八度』美味泡芙免费卷！】
名额有限，先到先得哦
---
via: 「{encodenum(qq_id)}」
    '''

#@invite_from_user.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.current_key:
        session.args[session.current_key] = stripped_arg
    elif 'via' in stripped_arg:
        session.args['invite_by'] = decodenum(stripped_arg[stripped_arg.find('「')+1:stripped_arg.find('」')])
        print(session.args['invite_by'])


