from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123456")
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

Session_local = sessionmaker(bind=engine)

def get_db():
    db = Session_local()
    try:
        yield db
    finally:
        db.close()
