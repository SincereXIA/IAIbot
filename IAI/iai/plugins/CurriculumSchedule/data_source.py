# 导入:
from IAI.setup import *
from sqlalchemy import Integer, Column, String, create_engine, Time, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from IAI.DBdriver import DBSession
from datetime import datetime,timedelta,time
import time
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
    weekday = Column(Integer)
    place = Column(VARCHAR(100))
    teacher = Column(VARCHAR(100))
    other = Column(VARCHAR(100))
    begin_week = Column(Integer)
    end_week = Column(Integer)
    start_time = Column(Time)
    group_id = Column(Integer)


def getClassInfo(week, weekday,group_id, classnum):
    session = DBSession()
    curriculum = session.query(Curriculum).filter(
        Curriculum.group_id == group_id,
        Curriculum.weekday == weekday+1,
        Curriculum.begin_week <= week,
        Curriculum.end_week >= week,
        Curriculum.class_num == classnum
    ).first()
    session.close()
    info = {}
    info['subject'] = "微机原理"
    info['teacher'] = "张俊华"
    info['place'] = "C417"
    info['start_time'] = "18:00"
    info['end_time'] = "19:30"
    info['other'] = ""
    return curriculum

def getRecentClassInfo(time:datetime, group_id, timeLimit = None):
    # 获取当前周
    localtime = datetime.now()
    curriculumStart = datetime(2018,9,3)
    day = int(localtime.strftime("%j")) - int(curriculumStart.strftime("%j"))
    if day >= 0:
        week = day % 7
    else:
        week = day % -7

    #数据库
    session = DBSession()
    curriculums = session.query(Curriculum).order_by(Curriculum.class_num).\
        filter(
        Curriculum.group_id == group_id,
        Curriculum.weekday == localtime.weekday(),
        Curriculum.begin_week <= week,
        Curriculum.end_week >= week,
    )
    session.close()

    #为未定义课程时间生成时间
    summer_time = ['8:30','10:25','14:30','16:25']
    for item in summer_time:
        item = time.strptime(item,'%H:%M')
    for curriculum in curriculums:
        if not curriculum.start_time:
            curriculum.start_time = summer_time[int(curriculum.class_num)]
            #todo 夏令时和冬令时

    # 筛选
    result =[]
    for curriculum in curriculums:
        if curriculum.start_time.strftime("%H%M%S") >= localtime.strftime("%H%M%S"):
            if timeLimit:
                if curriculum.start_time.strftime("%H%M%S") <= \
                (localtime+timedelta(minutes = timeLimit)).strftime("%H%M%S"):
                    result.append(curriculum)
                    continue
            result.append(curriculum)

    return result[0]





