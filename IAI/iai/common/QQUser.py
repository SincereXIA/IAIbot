from sqlalchemy import Integer, Column, Boolean, VARCHAR, Date, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from IAI.DBdriver import DBSession
from datetime import datetime
from none import get_bot
import requests
import json

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class QQUser(Base):
    # 表的名字:
    __tablename__ = 'user_info'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    qq_id = Column(VARCHAR(100))
    group_id = Column(VARCHAR(100))
    nickname = Column(VARCHAR(100))
    group_card = Column(VARCHAR(100))
    sex = Column(VARCHAR(100))
    group_role = Column(VARCHAR(100))
    join_time = Column(DATETIME)


async def get_user_group(qq_id):
    session = DBSession()
    qqUser = session.query(QQUser).filter(QQUser.qq_id == qq_id).first()
    session.close()
    return qqUser.group_id

async def get_user(qq_id):
    session = DBSession()
    qqUser = session.query(QQUser).filter(QQUser.qq_id == qq_id).first()
    session.close()
    return qqUser

async def get_qq_user_info(qq_id):
    bot = get_bot()
    url = f'http://{bot.config.IP_ADDRESS}:{bot.config.IP_PORT}/get_stranger_info'
    re = requests.get(url, {'user_id': qq_id})
    userinfo = json.loads(re.text)['data']
    return userinfo