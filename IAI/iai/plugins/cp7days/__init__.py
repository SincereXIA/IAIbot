from none import on_command,CommandSession,get_bot
import requests
import json
import IAI.iai.plugins.cp7days.data_source as data_source


@on_command('cp7days', aliases=('一周',))
async def cp7days(session:CommandSession):
    url = 'http://127.0.0.1:5700/get_stranger_info'
    re = requests.get(url, {'user_id': session.ctx['user_id']})
    userinfo = json.loads(re.text)['data']
    if userinfo['sex'] == 'male': userinfo['sex'] = 1
    else: userinfo['sex'] = 2
    dbuser = await data_source.join_event(str(userinfo['user_id']),userinfo['nickname'],userinfo['sex'])
    if not dbuser:
        await session.send('你已经报名参加过本次活动了哦')
        return
    if userinfo['sex'] == 1: sex = '男生'
    else: sex = '女生'
    text = f'''
恭喜你报名成功 「一周 CP」
你的信息：
昵称：{userinfo['nickname']}
性别：{sex}

我们将会为你寻找 TA，配对完成，你将会收到通知
    '''
    await session.send(text)
    the_other = await data_source.find_the_other(userinfo['sex'])
    if the_other:
        await data_source.make_cp(dbuser,the_other)
        await find_the_other(dbuser,the_other)

async def find_the_other(user, the_other):
    bot = get_bot()
    ctx = {'message_type': 'private', 'self_id': bot.config.ROBOT_ID, 'user_id':user.qq_id}
    msg = f'''
为你匹配到了：{the_other.user_name}
即将为你们取得联系...
Ta 的 QQ 号是：{the_other.qq_id}
加 Ta 为好友吧，别忘了备注：「来自 一周 CP」
    '''
    await bot.send(ctx,msg)
    ctx = {'message_type': 'private', 'self_id': bot.config.ROBOT_ID, 'user_id': the_other.qq_id}
    msg = f'''
为你匹配到了：{user.user_name}
即将为你们取得联系
Ta 的 QQ 号是：{user.qq_id}
加 Ta 为好友吧，别忘了备注：「来自 一周 CP」
        '''
    await bot.send(ctx, msg)


