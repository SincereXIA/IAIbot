# 导入:
from IAI.setup import *
from sqlalchemy import Integer, Column, String, create_engine, Time, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from IAI.DBdriver import DBSession


def getClassInfo(week, weekday, classnum=None, nextclass=False):
    info = {}
    info['subject'] = "微机原理"
    info['teacher'] = "张俊华"
    info['place'] = "C417"
    info['start_time'] = "18:00"
    info['end_time'] = "19:30"
    info['other'] = ""
    return info


# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class Curriculum(Base):
    # 表的名字:
    __tablename__ = 'CurriculumSchedule'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    class_name = Column(VARCHAR(100))
    class_num = Column(Integer)
    place = Column(VARCHAR(100))
    teacher = Column(VARCHAR(100))
    other = Column(VARCHAR(100))
    begin_week = Column(Integer)
    end_week = Column(Integer)
    start_time = Column(Time)


session = DBSession()

curriculum = session.query(Curriculum).get(1)
print(curriculum.class_name)
