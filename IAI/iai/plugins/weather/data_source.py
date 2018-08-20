
async def get_weather_of_city(city:str)->str:
    url = "http://api.jirengu.com/getWeather.php?city="+city
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