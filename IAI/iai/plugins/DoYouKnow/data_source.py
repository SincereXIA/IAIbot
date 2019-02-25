from sqlalchemy import func, Integer, Column, TEXT, String, create_engine, Time, VARCHAR,Date
from sqlalchemy.ext.declarative import declarative_base
from IAI.DBdriver import DBSession
import requests
import json
import random

from datetime import datetime,timedelta

news_dict = {'update_time':datetime.now()-timedelta(days=10), 'top_news':[], 'wangyi':[], 'global':[], 'tech':[],'all':[]}


# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class DoYouKnow(Base):
    # 表的名字:
    __tablename__ = 'doyouknow'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    text = Column(TEXT)
    times = Column(Integer)
    ad_flag = Column(Integer)

async def get_do_you_know():

    session = DBSession()
    dyn = session.query(DoYouKnow).order_by(func.rand()).first()
    dyn.times += 1
    try:
        session.merge(dyn)
    except Exception:
        session.rollback()
    session.close()
    result = {}
    result['text'] = dyn.text
    result['info'] = dyn.times
    return result

async def get_one_content():
    try:
        idlist = requests.get('http://v3.wufazhuce.com:8000/api/onelist/idlist')
        idlist = json.loads(idlist.text)
        id = int(idlist['data'][0])
    except Exception:
        id = 4100
    try:
        content = requests.get(f'http://v3.wufazhuce.com:8000/api/onelist/{id-random.randint(0,300)}/0')
        content = json.loads(content.text)
        result = {}
        result['text'] = content['data']['content_list'][0]['forward']
        result['info'] = content['data']['content_list'][0]['words_info']
    except Exception:
        result = {}
        result['text'] = "希望你孤独又不走运，没人喜欢，这样只剩我可以喜欢。希望你所到之处潮闷落雨，于是想念有我的好天。要你在精彩美貌又友善的世界仍然喜欢我，当然也好，可是完全没有这样的信心，也决不肯冒那样的险。要是我有钱，就把你买回家。要是我做官，就把你关进监牢去。"
        result['info'] = "苏方"
    return result




def news_refresh():
    # 基本Url
    base_url = 'http://c.3g.163.com/nc/article/list/T1467284926140/0-20.html'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }
    try:

        # 获取 JSON 数据
        r = requests.get(base_url,headers = headers)

        results = r.json().popitem()[1]

        for result in results[1:]:
            news_dict.get("wangyi").append({'title':result.get("title"),
                                            'digest':result.get("digest"),
                                            'url':result.get("url")})
    except Exception as e:
        print("网易新闻获取失败：",e)

    try:
        url = ('https://newsapi.org/v2/top-headlines?'
               'country=cn&'
               'apiKey=0be5a2944d0e4595bafc67da16a5e641')
        response = requests.get(url)
        results = response.json().get('articles')
        for result in results:
            news_dict.get("global").append({'title': result.get("title"),
                                            'digest': result.get("description"),
                                            'url': result.get("url")})
    except Exception as e:
        print("全球新闻获取失败",e)


    try:
        url = ('https://newsapi.org/v2/top-headlines?'
               'country=cn&category=technology&'
               'apiKey=0be5a2944d0e4595bafc67da16a5e641')
        response = requests.get(url)
        results = response.json().get('articles')
        for result in results:
            news_dict.get("tech").append({'title': result.get("title"),
                                            'digest': result.get("description"),
                                            'url': result.get("url")})
    except Exception as e:
        print("科技新闻获取失败",e)

    try:

        news_dict['update_time'] =  datetime.now()

        news_dict['top_news'].extend(news_dict['wangyi'][0:2])
        news_dict['top_news'].extend(news_dict['global'][0:1])
        news_dict['top_news'].extend(news_dict['tech'][0:1])

        news_dict['all'].extend(news_dict['global'])
        news_dict['all'].extend(news_dict['tech'])
    except Exception as e:
        print("新闻更新失败",e)

    print("[info] news refresh success")


def get_news():
    if datetime.now()- news_dict['update_time'] > timedelta(hours=1):
        news_refresh()
    return news_dict
