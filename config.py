import os
import sys
import warnings
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
if SECRET_KEY == "your-secret-key-change-in-production":
    warnings.warn(
        "⚠️  安全警告: 使用默认 SECRET_KEY！在生产环境中必须通过环境变量设置 SECRET_KEY。",
        UserWarning,
        stacklevel=2
    )
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "student")
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "5"))

REQUIRED_ENV_VARS = ["DB_PASSWORD"]
MISSING_VARS = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
if MISSING_VARS:
    warnings.warn(
        f"⚠️  配置警告: 以下必需的环境变量未设置: {', '.join(MISSING_VARS)}",
        UserWarning,
        stacklevel=2
    )
