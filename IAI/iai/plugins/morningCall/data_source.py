import requests
import json
import random
from sqlalchemy import func, Integer, Column, TEXT, String, create_engine, Time, VARCHAR,Date
from sqlalchemy.ext.declarative import declarative_base
from IAI.DBdriver import DBSession
from IAI.iai.plugins.CurriculumSchedule.data_source import getClassInfoFromTime
from datetime import datetime

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

async def get_one_content():
    idlist = requests.get('http://v3.wufazhuce.com:8000/api/onelist/idlist')
    idlist = json.loads(idlist.text)
    id = int(idlist['data'][0])
    content = requests.get(f'http://v3.wufazhuce.com:8000/api/onelist/{id-random.randint(0,300)}/0')
    content = json.loads(content.text)
    result = {}
    result['text'] = content['data']['content_list'][0]['forward']
    result['info'] = content['data']['content_list'][0]['words_info']
    return result


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

async def get_today_class_info(group_id):
    localtime = datetime.now()
    full_infos = getClassInfoFromTime(localtime,group_id)
    info = []
    class_num = ['1-2','3-4','5-6','7-8','9-10']
    for full_info in full_infos:
        i = {}
        i['class_num'] = class_num[full_info.class_num-1]
        i['class_name'] = full_info.class_name
        info.append(i)

    return info

