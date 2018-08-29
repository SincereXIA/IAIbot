import none
from none import on_command,CommandSession
from . import data_source
@on_command('doyouknow')
async def DoYouKnow(session:CommandSession):
    msg = await data_source.get_do_you_know()
    await session.send(str(msg))

async def do_you_know():
    data = await data_source.get_do_you_know()
    msg = f'''
你知道吗：
    {data['text']}
    '''
    return msg
