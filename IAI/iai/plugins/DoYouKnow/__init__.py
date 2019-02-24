import nonebot
from nonebot import on_command,CommandSession
from . import data_source
import random

@on_command('doyouknow')
async def test_dyn(session:CommandSession):
    await session.send(await do_you_know())


async def do_you_know():
    try:
        choice = random.randint(1,5)
        if choice == 3:
            data = await data_source.get_do_you_know()
            data = data['text']
        elif choice > 3:
            data = await news_msg()
        else:
            data = await data_source.get_one_content()
            data = data['text']

        if choice <= 3:
            msg = f'''
你知道吗：
   {data.strip()}
            '''
        else:
            msg = f'''
{data.strip()}
            '''
        return msg
    except Exception as e:
        return ""


async def one_msg():
    data = await data_source.get_one_content()
    msg = f'''
    「{data['text']}」
    —— {data['info']}
        '''
    return msg

async def news_msg():
    data = data_source.get_news().get('all')
    choice = random.randint(0, len(data)-1)
    msg = f'''
{data[choice]['title']}
--- {data[choice]['digest']}
{data[choice]['url']}

        '''
    return msg

