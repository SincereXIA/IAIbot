from none import on_request,RequestSession,get_bot,on_notice,NoticeSession
import time
import random
import requests,json
from . import data_source
@on_request('friend')
async def _(session: RequestSession):
    time.sleep(random.randrange(2,5))
    await session.approve()
    msg = f'''
真好呀，你没有错过我。

这个地球上有几十亿人口， 两个人相遇的概率是千万分之一。

跟我走，让小概率的相遇发生。

正在开放：一周CP

.......

回复：一周
报名参加本次「一周 CP」

感谢相遇。祝好 ：）
    '''
    await session.send(msg)
    return

@on_notice('group_increase')
async def _(session: NoticeSession):
    time.sleep(random.randrange(2, 5))
    url = 'http://127.0.0.1:5700/get_group_member_list'
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
    ctx = {'message_type': 'group', 'self_id': get_bot().config.ROBOT_ID, 'group_id': session.ctx['group_id']}
    await get_bot().send(ctx,msg)

@on_request('group')
async def _(session:RequestSession):
    time.sleep(random.randrange(2, 5))
    await session.approve()