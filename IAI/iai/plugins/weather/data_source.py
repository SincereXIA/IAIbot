import requests
import json
from nonebot import get_bot
from datetime import datetime, timedelta

weather_results = {}


async def get_weather_of_city(city: str) -> str:
    url = "https://search.heweather.com/find"
    print(url)
    try:
        r = requests.get(url)
        print(r.content)
        if json.loads(r.content)["status"] != "success":
            raise ConnectionError
        results = json.loads(r.content)['results'][0]
        weather = results['weather_data'][0]
        s = f'''
        {results['currentCity']}的天气情况
        {weather['date']}
        天气：{weather['weather']}
        风向：{weather['wind']}
        气温：{weather['temperature']}
        '''
    except ConnectionError:
        s = "未获取到天气信息，请检查输入是否有误"
    except Exception as e:
        s = e
    return str(s)


async def get_weather_of_city_HF(city: str) -> str:
    url = 'https://free-api.heweather.com/s6/weather?parameters'
    try:
        r = requests.get(url, {"key": f'{get_bot().config.HF_WEATHER_KEY}', "location": city})
        results = json.loads(r.text)['HeWeather6'][0]
        if results['status'] != "ok":
            raise ConnectionError
        weatherNow = results['now']
        s = f'''
        {results['basic']['location']}的天气情况
        
        当前天气：
        ''' + Now_foreast(results) + '''
        今日预报
        ''' + daily_foreast(results)
    except ConnectionError:
        s = "未获取到天气信息，请检查输入是否有误"
    except Exception as e:
        s = e
    return str(s)


async def get_forecast(city: str):
    pass
    # todo 获取预报信息


async def should_forecast(city: str, group):
    pass
    # todo 判断是否需要预报


def daily_foreast(results):
    daily = results['daily_forecast'][0]
    try:
        foreast = f'''
        温度：{daily['tmp_min']}~{daily['tmp_max']}℃
        白天：{daily['cond_txt_d']}
        晚间：{daily['cond_txt_n']}
        风向：{daily['wind_dir']} {daily['wind_sc']}级
        相对湿度：{daily['hum']}
        降水概率：{daily['pop']}
        降水量：{daily['pcpn']}
        紫外线强度指数：{daily['uv_index']}
        '''
    except Exception as ex:
        foreast = "预报获取失败" + str(ex)

    return foreast


def Now_foreast(results):
    now = results['now']
    try:
        foreast = f'''
        {now['cond_txt']}
        体感温度：{now['fl']}℃
        风向：{now['wind_dir']} {now['wind_sc']}级
        相对湿度：{now['hum']}
        '''
    except Exception as ex:
        foreast = "预报获取失败" + str(ex)

    return foreast


async def get_weather_forecast(city: str):
    url = 'https://free-api.heweather.com/s6/weather?parameters'
    global weather_results
    if city in weather_results.keys() and \
            weather_results[city]['update_time'] > datetime.now() - timedelta(minutes=10):
        return weather_results[city]

    try:
        weather_results[city] = {}
        r = requests.get(url, {"key": f'{get_bot().config.HF_WEATHER_KEY}', "location": city})
        rs = json.loads(r.text)['HeWeather6'][0]
        weather_results[city]['status'] = rs['status']
        if rs['status'] != "ok":
            raise ConnectionError
    except ConnectionError:
        weather_results[city]['debug_info'] = "未获取到天气信息，请检查输入是否有误"
        return
    except Exception as e:
        weather_results[city]['debug_info'] = e
        return
    weather_results[city]['update_time'] = datetime.now()
    weather_results[city]['today_forecast'] = rs['daily_forecast'][0]
    """
    {'cond_code_d': '101', 
    'cond_code_n': '101', 
    'cond_txt_d': '多云', 
    'cond_txt_n': '多云', 
    'date': '2018-08-28', 
    'hum': '47', 
    'mr': '20:29', 
    'ms': '07:33', 
    'pcpn': '0.0', 
    'pop': '1', 
    'pres': '1009', 
    'sr': '06:15', 
    'ss': '19:14', 
    'tmp_max': '34', 
    'tmp_min': '23', 
    'uv_index': '5', 
    'vis': '20', 
    'wind_deg': '27', 
    'wind_dir': '东北风', 
    'wind_sc': '1-2', 
    'wind_spd': '4'}
  """
    weather_results[city]['hourly'] = rs['hourly']
    """
    weather_results[city]['hourly'] = \
[{'cloud': '13', 
'cond_code': '101', 
'cond_txt': '大雨',
'dew': '15', 
'hum': '41', 
'pop': '60',
'pres': '1005', 
'time': '2018-08-31 13:00', 
'tmp': '33', 
'wind_deg': '96', 
'wind_dir': '东风', 
'wind_sc': '3-4', 
'wind_spd': '24'}, 
{'cloud': '12', 'cond_code': '100', 'cond_txt': '小雨', 'dew': '15', 'hum': '36', 'pop': '40', 'pres': '1003', 'time': '2018-08-31 16:00', 'tmp': '33', 'wind_deg': '86', 'wind_dir': '东风', 'wind_sc': '3-4', 'wind_spd': '24'}, {'cloud': '20', 'cond_code': '100', 'cond_txt': '晴', 'dew': '16', 'hum': '44', 'pop': '0', 'pres': '1004', 'time': '2018-08-31 19:00', 'tmp': '30', 'wind_deg': '95', 'wind_dir': '东风', 'wind_sc': '3-4', 'wind_spd': '21'}, {'cloud': '28', 'cond_code': '100', 'cond_txt': '晴', 'dew': '16', 'hum': '53', 'pop': '0', 'pres': '1007', 'time': '2018-08-31 22:00', 'tmp': '29', 'wind_deg': '99', 'wind_dir': '东风', 'wind_sc': '3-4', 'wind_spd': '15'}, {'cloud': '31', 'cond_code': '100', 'cond_txt': '晴', 'dew': '16', 'hum': '65', 'pop': '0', 'pres': '1008', 'time': '2018-09-01 01:00', 'tmp': '27', 'wind_deg': '92', 'wind_dir': '东风', 'wind_sc': '3-4', 'wind_spd': '16'}, {'cloud': '67', 'cond_code': '101', 'cond_txt': '多云', 'dew': '16', 'hum': '74', 'pop': '0', 'pres': '1009', 'time': '2018-09-01 04:00', 'tmp': '25', 'wind_deg': '98', 'wind_dir': '东风', 'wind_sc': '3-4', 'wind_spd': '20'}, {'cloud': '66', 'cond_code': '101', 'cond_txt': '多云', 'dew': '17', 'hum': '74', 'pop': '0', 'pres': '1010', 'time': '2018-09-01 07:00', 'tmp': '25', 'wind_deg': '83', 'wind_dir': '东风', 'wind_sc': '1-2', 'wind_spd': '2'}, {'cloud': '81', 'cond_code': '101', 'cond_txt': '多云', 'dew': '16', 'hum': '56', 'pop': '0', 'pres': '1010', 'time': '2018-09-01 10:00', 'tmp': '29', 'wind_deg': '115', 'wind_dir': '东南风', 'wind_sc': '3-4', 'wind_spd': '14'}]
"""
    weather_results[city]['lifestyle'] = rs['lifestyle']
    """
0 = {dict} {'type': 'comf', 'brf': '较不舒适', 'txt': '白天天气多云，同时会感到有些热，不很舒适。'}
1 = {dict} {'type': 'drsg', 'brf': '炎热', 'txt': '天气炎热，建议着短衫、短裙、短裤、薄型T恤衫等清凉夏季服装。'}
2 = {dict} {'type': 'flu', 'brf': '少发', 'txt': '各项气象条件适宜，发生感冒机率较低。但请避免长期处于空调房间中，以防感冒。'}
3 = {dict} {'type': 'sport', 'brf': '较不宜', 'txt': '天气较好，无雨水困扰，但考虑气温很高，请注意适当减少运动时间并降低运动强度，运动后及时补充水分。'}
4 = {dict} {'type': 'trav', 'brf': '较适宜', 'txt': '天气较好，温度较高，天气较热，但有微风相伴，还是比较适宜旅游的，不过外出时要注意防暑防晒哦！'}
5 = {dict} {'type': 'uv', 'brf': '中等', 'txt': '属中等强度紫外线辐射天气，外出时建议涂擦SPF高于15、PA+的防晒护肤品，戴帽子、太阳镜。'}
6 = {dict} {'type': 'cw', 'brf': '较适宜', 'txt': '较适宜洗车，未来一天无雨，风力较小，擦洗一新的汽车至少能保持一天。'}
7 = {dict} {'type': 'air', 'brf': '中', 'txt': '气象条件对空气污染物稀释、扩散和清除无明显影响，易感人群应适当减少室外活动时间。'}
    """
    return weather_results[city]

async def get_today_weather_info(city):
    weather = await get_weather_forecast(city)
    info = {}
    info['cond_d'] = weather['today_forecast']['cond_txt_d']
    info['pop'] = weather['today_forecast']['pop']
    info['tmp_max'] = weather['today_forecast']['tmp_max']
    info['tmp_min'] = weather['today_forecast']['tmp_min']
    info['comf'] = weather['lifestyle'][0]['txt']
    info['drsg'] = weather['lifestyle'][1]['txt']
    info['uv'] = weather['lifestyle'][5]['txt']

    return info

async def get_weather_hourly(city):
    weather_hourly = (await get_weather_forecast(city))['hourly']
    return weather_hourly

