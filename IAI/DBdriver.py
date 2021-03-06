"""
IAIbot 数据库模块
完成数据库身份验证和链接，初始化数据库连接池，创建 DBSession

author: 16030199025 张俊华
"""
from sqlalchemy import Integer,Column, String, create_engine, Time, VARCHAR
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy.ext.declarative import declarative_base
from IAI.setup import *

# 初始化数据库连接:
engine = create_engine(f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}:{DB_PORT}/{DB_TABLE}')
# 创建DBSession类型:
DBSession = scoped_session(sessionmaker(bind=engine))
# todo 执行103次session创建会使 QueuePool 出现 TimeoutError，使用 scoped 解决
