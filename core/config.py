from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+mysqldb://root:password@localhost:3306/example_db")
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"


settings = Settings()