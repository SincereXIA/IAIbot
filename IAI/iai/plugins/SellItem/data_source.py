from datetime import datetime
from sqlalchemy import DateTime, BOOLEAN, Integer, Column, TEXT, String, create_engine, Time, VARCHAR, Date
from sqlalchemy.ext.declarative import declarative_base
from IAI.DBdriver import DBSession
from IAI.iai.common.QQUser import get_user

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class SellItem(Base):
    # 表的名字:
    __tablename__ = 'sellitem'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    item_name = Column(VARCHAR(100))
    item_info = Column(TEXT)
    seller_id = Column(VARCHAR(100))
    seller_name = Column(VARCHAR(100))
    is_onsell = Column(BOOLEAN)
    from_group_id = Column(VARCHAR(100))
    add_time = Column(DateTime)


async def add_item(item_name, item_info, seller_id, from_group_id=None, add_time=None, **kw):
    if add_time is None:
        add_time = datetime.now()
    item = SellItem(item_name = item_name, item_info = item_info, seller_id=seller_id,
                    from_group_id = from_group_id, add_time=add_time)
    session = DBSession()
    session.add(item)
    session.commit()
    session.close()

async def get_item_list(key_words = None):
    like_str = ""
    session = DBSession()
    results = []
    if key_words:
        for word in key_words:
            for c in word:
                like_str += f'%{c}'
                like_str += '%'
            results.extend(session.query(SellItem).filter(

                SellItem.item_name.like(like_str)
            ).order_by(SellItem.add_time).all())
    else:
        results.extend(session.query(SellItem).filter(
        ).order_by(SellItem.add_time).all())

    session.close()

    return sorted(list(set([i for i in results])), key=lambda x:x.add_time)
async def get_item(id):
    session = DBSession()
    item = session.query(SellItem).filter(SellItem.id == id).first()
    session.close()
    return item

