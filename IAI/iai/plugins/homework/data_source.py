from datetime import date
from sqlalchemy import Integer, Column, TEXT, String, create_engine, Time, VARCHAR, Date
from sqlalchemy.ext.declarative import declarative_base
from IAI.DBdriver import DBSession

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class Homework(Base):
    # 表的名字:
    __tablename__ = 'homework'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer)
    subject_name = Column(VARCHAR)
    content = Column(TEXT)
    assign_for = Column(VARCHAR)
    added_date = Column(Date)
    end_date = Column(Date)
    add_by = Column(VARCHAR)


async def get_homework_info(group_id, date: date, subject_name=None):
    like_str = ""
    if subject_name is not None:
        for c in subject_name:
            like_str += f'%{c}'
    like_str += '%'

    session = DBSession()
    results = session.query(Homework).filter(
        Homework.group_id == group_id,
        Homework.added_date <= date,
        Homework.end_date >= date,
        Homework.subject_name.like(like_str)
    ).all()
    session.close()
    return results


async def add_homework_info(group_id, subject_name, content, end_date,
                            assign_for=None, added_date=None,
                            add_by=None):
    if added_date is None:
        added_date = date.today()
    homework = Homework(group_id=group_id, subject_name=subject_name,
                        content=content, end_date=end_date,
                        assign_for=assign_for, added_date=added_date,
                        add_by=add_by)
    session = DBSession()
    session.add(homework)
    session.commit()
    session.close()