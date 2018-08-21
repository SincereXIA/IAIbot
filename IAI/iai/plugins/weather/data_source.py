import requests
import json
async def get_weather_of_city(city:str)->str:
    url = "https://search.heweather.com/find"
    print(url)
    try:
        r = requests.get(url)
        print(r.content)
        if json.loads(r.content)["status"]!="success":
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

async def get_weather_of_city_HF(city:str)->str:
    url = 'https://free-api.heweather.com/s6/weather?parameters'
    try:
        r = requests.get(url,{"key":'1d6c2a345f0843e7ae37a829466651de',"location":city})
        results = json.loads(r.text)['HeWeather6'][0]
        if results['status'] != "ok":
            raise ConnectionError
        weatherNow = results['now']
        s = f'''
        {results['basic']['location']}的天气情况
        
        当前天气：
        ''' + Now_foreast(results)+'''
        今日预报
        '''+daily_foreast(results)
    except ConnectionError:
        s = "未获取到天气信息，请检查输入是否有误"
    except Exception as e:
        s = e
    return str(s)

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
