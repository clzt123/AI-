from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
#连接数据库
SQL_URL = "mysql+pymysql://root:123456@localhost/student"
# 创建数据库引擎
engine = create_engine(SQL_URL,pool_size=5)

# 得到Base基类，写数据库表类必须继承它
Base = declarative_base()
#创建会话工厂
Session_local = sessionmaker(bind=engine)

# 数据库会话生成函数
def get_db():
    db = Session_local()
    try:
        yield db #生成器函数，专门用于fastapi依赖注入（每次请求产生一个会话，用完自动关闭）
    finally:
        db.close()   #用完就关

