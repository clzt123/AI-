from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_POOL_SIZE
from urllib.parse import quote_plus

SQL_URL = f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD or '')}@{DB_HOST}/{DB_NAME}"

engine = create_engine(
    SQL_URL,
    pool_size=DB_POOL_SIZE,
    max_overflow=10,
    pool_recycle=3600,
    pool_pre_ping=True
)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

def get_db() -> Generator[Session, None, None]:
    """获取数据库会话依赖，确保会话使用后自动关闭"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
