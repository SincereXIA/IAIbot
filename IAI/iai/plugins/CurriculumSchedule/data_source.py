from sqlalchemy import Integer, Column, String, create_engine, Time, VARCHAR, Date
from sqlalchemy.ext.declarative import declarative_base
from IAI.DBdriver import DBSession
from datetime import datetime, timedelta, time

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class Curriculum(Base):
    # 表的名字:
    __tablename__ = 'curriculumschedule'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    class_name = Column(VARCHAR(100))
    group_name = Column(VARCHAR(100))
    class_num = Column(Integer)
    weekday = Column(Integer)
    place = Column(VARCHAR(100))
    teacher = Column(VARCHAR(100))
    other = Column(VARCHAR(100))
    begin_week = Column(Integer)
    end_week = Column(Integer)
    start_time = Column(Time)
    group_id = Column(Integer)
    last_notify_date = Column(Date)


def getClassInfoFromTime(time: datetime, group_id, classnums=None) -> list:
    if classnums is None:
        classnums = [1, 2, 3, 4, 5]

    weekday = time.weekday()
    week = get_session_week(time)
    return getClassInfo(week, weekday, group_id, classnums)

def getClassInfo(week, weekday, group_id, classnums) -> list:
    session = DBSession()
    curriculums = []
    for classnum in classnums:
        rs = session.query(Curriculum).filter(
            Curriculum.group_id == group_id,
            Curriculum.weekday == weekday + 1,
            Curriculum.begin_week <= week,
            Curriculum.end_week >= week,
            Curriculum.class_num == classnum
        ).all()
        if rs is not None:
            for r in rs:
                curriculums.append(r)
    # 为未定义课程时间生成时间
    # 获取当前周
    localtime = datetime.now()
    # 为未定义课程时间生成时间
    summer_time = [time(8, 30), time(10, 25), time(14, 30), time(16, 25), time(19, 00), ]
    winter_time = [time(8, 30), time(10, 25), time(14, 00), time(16, 55), time(18, 30), ]

    for curriculum in curriculums:
        if not curriculum.start_time:
            if localtime.month < 10:
                curriculum.start_time = summer_time[int(curriculum.class_num) - 1]
            else:
                curriculum.start_time = winter_time[int(curriculum.class_num) - 1]
    session.close()
    return curriculums


def getRecentClassInfo(recent_time: datetime, group_id, timeLimit=None):
    # 获取当前周
    localtime = datetime.now()
    week = get_session_week(localtime)

    # 数据库
    session = DBSession()
    curriculums = session.query(Curriculum).order_by(Curriculum.class_num). \
        filter(
        Curriculum.group_id == group_id,
        Curriculum.weekday == localtime.weekday() + 1,
        Curriculum.begin_week <= week,
        Curriculum.end_week >= week,
    )
    session.close()

    # 为未定义课程时间生成时间
    summer_time = [time(8, 30), time(10, 25), time(14, 30), time(16, 25), time(19, 00), ]
    winter_time = [time(8, 30), time(10, 25), time(14, 00), time(16, 55), time(18, 30), ]

    for curriculum in curriculums:
        if not curriculum.start_time:
            if localtime.month < 10:
                curriculum.start_time = summer_time[int(curriculum.class_num) - 1]
            else:
                curriculum.start_time = winter_time[int(curriculum.class_num) - 1]

    # 筛选
    result = []
    for curriculum in curriculums:
        if curriculum.start_time.strftime("%H%M%S") >= localtime.strftime("%H%M%S"):
            if timeLimit:
                if curriculum.start_time.strftime("%H%M%S") <= \
                        (localtime + timedelta(minutes=timeLimit)).strftime("%H%M%S"):
                    result.append(curriculum)
                    continue
                else:
                    continue
            result.append(curriculum)
    return result


def get_session_week(localtime):
    curriculumStart = datetime(2018, 9, 3)
    week = (int(localtime.strftime("%j")) - int(curriculumStart.strftime("%j"))) // 7
    return week
