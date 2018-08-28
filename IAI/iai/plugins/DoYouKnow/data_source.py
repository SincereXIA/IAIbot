from sqlalchemy import func, Integer, Column, TEXT, String, create_engine, Time, VARCHAR,Date
from sqlalchemy.ext.declarative import declarative_base
from IAI.DBdriver import DBSession


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