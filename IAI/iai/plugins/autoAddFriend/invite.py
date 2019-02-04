from none import get_bot,CommandSession,on_command
import requests
import json
from . import data_source
from IAI.iai.common.QQUser import get_qq_user_info

async def init_invite(session,user_id = None,call = True):
    bot = get_bot()
    try:
        userinfo = await get_qq_user_info(session.ctx['user_id'])
    except Exception:
        userinfo = {'user_id':session.ctx['user_id'], 'nickname':session.ctx['user_id']}

    await data_source.init_user_invite(str(userinfo['user_id']), userinfo['nickname'])
    if call:
        await session.send('''
真好呀，你没有错过我。

正在开放：月饼节试吃活动

.......

回复：试吃
或发送好友给你的口令
报名参加本次活动

感谢相遇。祝好 ：）
        ''')

@on_command('getsellcard')
async def get_sell_card(qq_id):
    #http://127.0.0.1/add_coupons?psw=xdncj123&serial=937734121&name=%E6%B5%8B%E8%AF%95&begin_time=2018-09-18%2009:26:04&&end_time=2018-09-19%2009:26:04
    url = 'http://nc.sumblog.cn/add_coupons'
    params = {
        'psw':'xdncj123',
        'serial':qq_id,
        'name':'内参君月饼节泡芙免费卷',
        'begin_time': '2018-09-20 00:26:04',
        'end_time':'2018-09-21 23:59:59',
        'amount':'免费',
        'intro': '''该优惠券仅限 香八度® 西安电子科技大学新校区 店使用，到店后点开上方优惠券，可免费领取一个美味泡芙，该优惠券使用一次后失效
优惠券使用时间 2018 年 9 月 20、21 日 16:00 至 21:00。每日泡芙数量为 150 个，送完即止'''
    }
    r = requests.get(url,params)
    if(r.status_code == 200):
        msg = f"""
不出我所料，你果然是西电人气王！
美味泡芙免费卷这就送上：
{r.text}
点开上方链接，我们「香八度」见！
        """
        bot = get_bot()
        ctx = {'message_type': 'private', 'self_id': bot.config.ROBOT_ID, 'user_id': qq_id}
        await bot.send(ctx, msg)

@on_command('测评')
async def ceping(session:CommandSession):
    await session.send('''
【欢迎在现场参与测评】
点击下方链接，参与内参君月饼节现场试吃测评
https://www.wjx.top/jq/28340363.aspx

主观题最好也填哦！
''')



