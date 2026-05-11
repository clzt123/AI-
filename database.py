from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os
from dotenv import load_dotenv
from typing import Generator

load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "student")
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "5"))

SQL_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

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
