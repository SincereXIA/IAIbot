import nonebot
from nonebot import on_command,CommandSession
from . import data_source
import random


async def do_you_know():
    choice = random.randint(1,3)
    if choice == 3:
        data = await data_source.get_do_you_know()
    else:
        data = await data_source.get_one_content()

    msg = f'''
你知道吗：
    {data['text']}
    '''
    return msg


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

