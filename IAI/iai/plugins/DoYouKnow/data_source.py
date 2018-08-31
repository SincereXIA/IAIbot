from sqlalchemy import func, Integer, Column, TEXT, String, create_engine, Time, VARCHAR,Date
from sqlalchemy.ext.declarative import declarative_base
from IAI.DBdriver import DBSession
import requests
import json
import random
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
    session.merge(dyn)
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