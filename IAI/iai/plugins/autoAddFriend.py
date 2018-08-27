from none import on_request,RequestSession

@on_request('friend')
async def _(session: RequestSession):
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
