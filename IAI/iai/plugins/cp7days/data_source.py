from sqlalchemy import Integer, Column, Boolean, VARCHAR,Date
from sqlalchemy.ext.declarative import declarative_base
from IAI.DBdriver import DBSession
# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class CPuser(Base):
    # 表的名字:
    __tablename__ = 'cp7day'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    qq_id = Column(VARCHAR(100))
    user_name = Column(VARCHAR(100))
    user_sex = Column(Integer)
    is_paired = Column(Boolean)
    paired_to = Column(Integer)

async def find_the_other(user_sex):
    if user_sex == 1:
        findsex = 2
    else:
        findsex = 1
    session = DBSession()
    theOther = session.query(CPuser).filter(
        CPuser.user_sex == findsex,
        CPuser.is_paired == 0,
    ).first()
    session.close()

    return theOther

async def join_event(user_id,nickname,sex):
    session = DBSession()
    dbuser = session.query(CPuser).filter(
        CPuser.qq_id == user_id
    ).first()
    if dbuser:
        session.close()
        return False
    cpuser = CPuser(qq_id = user_id, user_name=nickname,user_sex=sex,is_paired=False)
    session.add(cpuser)
    session.commit()
    session.close()
    session = DBSession()
    cpuser = session.query(CPuser).filter(
        CPuser.qq_id == user_id
    ).first()
    session.close()
    return cpuser

async def make_cp(user1, user2):
    session = DBSession()
    user1.is_paired = True
    user1.paired_to = user2.id
    user2.is_paired = True
    user2.paired_to = user1.id
    session.merge(user1)
    session.merge(user2)
    session.commit()
    session.close()
