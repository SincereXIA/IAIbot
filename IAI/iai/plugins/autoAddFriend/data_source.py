from sqlalchemy import Integer, Column, Boolean, VARCHAR, Date, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from IAI.DBdriver import DBSession
from datetime import datetime
from IAI.iai.common.GroupInfo import GroupInfo

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


async def add_QQUser(qq_id, nickname, group_id=None, group_card=None,
                     sex=None, group_role=None, **kw):
    session = DBSession()
    qqUser = session.query(QQUser).filter(QQUser.qq_id == qq_id).first()
    if qqUser:
        qqUser.nickname = nickname
        qqUser.group_id = group_id
        qqUser.group_role = group_role
        qqUser.sex = sex
        session.merge(qqUser)
        session.commit()
        session.close()
        return 1
    else:
        qqUser = QQUser(qq_id=qq_id, group_id=group_id, nickname=nickname,
                        group_card=group_card, sex=sex, group_role=group_role,
                        join_time=datetime.now())
        session.add(qqUser)
        session.commit()
        session.close()
        return 0



