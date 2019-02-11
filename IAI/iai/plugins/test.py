from nonebot import on_command,CommandSession
import nonebot
@on_command('test')
async def test(session:CommandSession):
    print(str(none._plugins))
    await session.send('[CQ:bface,id=1CDD748D516BFD27D30AF113419058E3,p=11958]')
