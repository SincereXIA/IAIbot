import none
from none import session, CommandSession,on_command
from . import data_source
@on_command('one')
async def one(session:CommandSession):
    data = await data_source.get_one_content()
    msg = f'''
    {data['text']}
    —— {data['info']}
    '''
    await session.send(msg)