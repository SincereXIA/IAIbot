from sqlalchemy import Integer, Column, Boolean, VARCHAR, Date, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from IAI.DBdriver import DBSession
from datetime import datetime

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class GroupInfo(Base):
    # 表的名字:
    __tablename__ = 'group_info'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    group_id = Column(VARCHAR(100))
    group_name = Column(VARCHAR(100))
    last_weather_notify = Column(DATETIME)
    is_morningcall_on = Column(Boolean)
    is_weather_notify_on = Column(Boolean)
    is_homework_daily_on = Column(Boolean)
    is_curriculumschedule_on = Column(Boolean)


async def get_group_info(group_id) -> GroupInfo:
    session = DBSession()
    group_info = session.query(GroupInfo).filter(GroupInfo.group_id == group_id).first()
    session.close()
    return group_info


async def add_group_info(group_id, group_name, last_weather_notify=None,
                         is_morningcall_on=True, is_curriculumschedule_on=True,
                         is_weather_notify_on=True, is_homework_daily_on=True):
    session = DBSession()
    group = session.query(GroupInfo).filter(GroupInfo.group_id == group_id).first()
    if group:
        group.group_id = group_id
        group.group_name = group_name
        group.is_morningcall_on = False
        group.is_curriculumschedule_on = False
        group.is_weather_notify_on = False
        group.is_homework_daily_on = False
        session.merge(group)
        session.commit()
        session.close()
        return 1
    else:
        group = GroupInfo(group_id=group_id, group_name=group_name, last_weather_notify=last_weather_notify,
                          is_morningcall_on=is_morningcall_on, is_curriculumschedule_on=is_curriculumschedule_on,
                          is_weather_notify_on=is_weather_notify_on, is_homework_daily_on=is_homework_daily_on)
        session.add(group)
        session.commit()
        session.close()
        return 0


async def update_last_weather_notify(group_id, last_weather_notify):
    session = DBSession()
    group = session.query(GroupInfo).filter(GroupInfo.group_id == group_id).first()
    group.last_weather_notify = last_weather_notify
    session.merge(group)
    session.commit()
    session.close()



async def get_all_group_info():
    try:
        session = DBSession()
        group = session.query(GroupInfo).all()
        session.close()
    except Exception as e:
        raise RuntimeError('更新notify时间时失败：' + str(e))
    return group
