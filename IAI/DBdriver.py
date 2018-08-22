from sqlalchemy import Integer,Column, String, create_engine, Time, VARCHAR
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from IAI.setup import *

# 初始化数据库连接:
engine = create_engine(f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}:{DB_PORT}/{DB_TABLE}')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)