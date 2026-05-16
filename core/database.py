from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL数据库连接配置
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/osatable"

# 使用auth_plugin_map配置认证插件
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"auth_plugin_map": {"caching_sha2_password": "mysql_native_password"}}, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 数据库依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()