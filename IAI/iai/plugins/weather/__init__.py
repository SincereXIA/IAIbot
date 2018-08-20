# coding=utf-8


from none import  on_command, CommandSession
from .data_source import get_weather_of_city

@on_command('weather', aliases=('天气',))
async def weather(session: CommandSession):

    city = session.get('city', prompt='请输入城市')
    ather_report = await get_weather_of_city(city)

    await session.send(ather_report)

@weather.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.current_key:
        session.args[session.current_key] = stripped_arg

    elif stripped_arg:
        session.args['city'] = stripped_arg


