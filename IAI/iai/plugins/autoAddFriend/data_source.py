from sqlalchemy import Integer, Column, Boolean, VARCHAR, Date, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from IAI.DBdriver import DBSession
from datetime import datetime
from IAI.iai.common.GroupInfo import GroupInfo
from . import invite
from IAI.iai.common.QQUser import get_qq_user_info

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
        if(group_id):
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

class User_invite(Base):
    # 表的名字:
    __tablename__ = 'user_invite'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    qq_id = Column(VARCHAR(100))
    nickname = Column(VARCHAR(100))
    invite_by = Column(VARCHAR(100))
    join_time = Column(DATETIME)

async def init_user_invite(qq_id,nickname):
    session = DBSession()
    user_invite = session.query(User_invite).filter(User_invite.qq_id == qq_id).first()
    if user_invite:
        session.close()
        return
    else:
        user_invite = User_invite(qq_id=qq_id,nickname=nickname,join_time=datetime.now())
        session.add(user_invite)
        session.commit()
        session.close()


async def invite_by(qq_id, invite_by):
    """
    更新用户的邀请者
    :param qq_id:
    :param invite_by:
    :return:
    """
    session = DBSession()
    user_invite = session.query(User_invite).filter(User_invite.qq_id == qq_id).first()
    if not user_invite:
        session.close()
        await init_user_invite(qq_id=qq_id,nickname= await get_qq_user_info(qq_id))
        invite_by(qq_id,invite_by)
    else:
        if not user_invite.invite_by:
            user_invite.invite_by = invite_by
        else:
            raise RuntimeError
        session.merge(user_invite)
        session.commit()
        # 判断是否邀请到足够人数
        invite_user_num = session.query(User_invite).filter(User_invite.invite_by == invite_by).count()
        if invite_user_num == 3:
            await invite.get_sell_card(invite_by)

        session.close()
        return True




async def get_user_invite(qq_id):
    """
    通过 qq 号，找到用户表项
    :param qq_id:
    :return:
    """
    session = DBSession()
    user_invite = session.query(User_invite).filter(User_invite.qq_id == qq_id).first()
    if user_invite:
        session.close()
        return user_invite
    else:
        raise RuntimeError



