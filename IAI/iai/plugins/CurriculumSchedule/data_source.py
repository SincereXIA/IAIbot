from sqlalchemy import Integer, Column, String, create_engine, Time, VARCHAR, Date
from sqlalchemy.ext.declarative import declarative_base
from IAI.DBdriver import DBSession
from datetime import datetime, timedelta, time
from sqlalchemy import and_, or_
import nonebot
import copy

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
    rs = session.query(Curriculum).filter(
        Curriculum.group_id == group_id,
        Curriculum.weekday == weekday + 1,
        Curriculum.begin_week <= week,
        Curriculum.end_week >= week,
        or_(*[Curriculum.class_num == i for i in classnums])
    ).order_by(Curriculum.class_num).order_by(Curriculum.group_name).all()
    #session.rollback()
    session.close()
    if rs is not None:
        for r in rs:
            curriculums.append(r)
    # 为未定义课程时间生成时间
    # 获取当前周
    localtime = datetime.now()
    # 为未定义课程时间生成时间
    summer_time = [time(8, 30), time(10, 25), time(14, 30), time(16, 25), time(19, 30), ]
    winter_time = [time(8, 30), time(10, 25), time(14, 00), time(15, 55), time(19, 00), ]

    for curriculum in curriculums:
        curriculum.group_name = [curriculum.group_name]
        # if not curriculum.start_time:
        if 10 > localtime.month >= 5:
            curriculum.start_time = summer_time[int(curriculum.class_num) - 1]
        else:
            curriculum.start_time = winter_time[int(curriculum.class_num) - 1]
    merge_curriculums = []
    for i in range(len(curriculums) - 1):
        if curriculums[i].class_name == curriculums[i + 1].class_name and \
                curriculums[i].class_num == curriculums[i + 1].class_num:
            curriculums[i + 1].group_name.extend(curriculums[i].group_name)
        else:
            merge_curriculums.append(curriculums[i])

    if curriculums:
        merge_curriculums.append(curriculums[len(curriculums)-1])


    return merge_curriculums


async def getRecentClassInfo(recent_time: datetime, group_id, timeLimit=None, from_schedule = False):
    # 获取当前周
    localtime = datetime.now()
    week = get_session_week(localtime)

    # 数据库
    session = DBSession()
    curriculums = session.query(Curriculum). \
        filter(
        Curriculum.group_id == group_id,
        Curriculum.weekday == localtime.weekday() + 1,
        Curriculum.begin_week <= week,
        Curriculum.end_week >= week,
    ).order_by(Curriculum.class_num, Curriculum.group_name).all()
    #session.rollback()
    session.close()

    # 为未定义课程时间生成时间
    summer_time = [time(8, 30), time(10, 25), time(14, 30), time(16, 25), time(19, 30), ]
    winter_time = [time(8, 30), time(10, 25), time(14, 00), time(15, 55), time(19, 00), ]

    for curriculum in curriculums:
        # if not curriculum.start_time:
        if 10 > localtime.month >= 5:
            curriculum.start_time = summer_time[int(curriculum.class_num) - 1]
        else:
            curriculum.start_time = winter_time[int(curriculum.class_num) - 1]

    curriculums_cpy = copy.deepcopy(curriculums)

    if from_schedule:
        # 筛选
        result = []
        for curriculum in curriculums:
            if curriculum.start_time.strftime("%H%M%S") >= localtime.strftime("%H%M%S"):
                if timeLimit:
                    if curriculum.start_time.strftime("%H%M%S") <= \
                            (localtime + timedelta(minutes=timeLimit)).strftime("%H%M%S"):
                        result.append(curriculum)
                else:
                    result.append(curriculum)
        return result

    # 筛选
    result = []
    for curriculum in curriculums_cpy:
        curriculum.group_name = [curriculum.group_name]
        if curriculum.start_time.strftime("%H%M%S") >= localtime.strftime("%H%M%S"):
            if timeLimit:
                if curriculum.start_time.strftime("%H%M%S") <= \
                        (localtime + timedelta(minutes=timeLimit)).strftime("%H%M%S"):
                    result.append(curriculum)
            else:
                if not result:
                    result.append(curriculum)
                elif curriculum.class_num == result[0].class_num:
                    result.append(curriculum)

    merge_curriculums = []
    for i in range(len(result) - 1):
        if result[i].class_name == result[i + 1].class_name and \
                result[i].class_num == result[i + 1].class_num:
            result[i + 1].group_name.extend(result[i].group_name)
        else:
            merge_curriculums.append(result[i])

    if result:
        merge_curriculums.append(result[len(result) - 1])

    return merge_curriculums


def get_session_week(localtime):
    # curriculumStart = datetime(2019, 2, 25)
    [year, month, day] = nonebot.get_bot().config.SEMESTER_START.split('-')
    curriculumStart = datetime(int(year), int(month), int(day))
    week = (int(localtime.strftime("%j")) -
            int(curriculumStart.strftime("%j"))) // 7 + 1
    return week
