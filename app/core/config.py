import os
from typing import List 
from dotenv import load_dotenv, find_dotenv
from core.static_data import messages as static
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field
from pathlib import Path 

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"



class Settings(BaseSettings):
    # App Settings
    ENV: str = "production"
    LOG_LEVEL: str = "INFO"
    TG_ALLOWED_MESSAGES: List[str] = ["/start"] + static.as_list()
    TG_TOKEN: str 
    # Database Settings
    DB_MANAGER: str = "postgresql" # or mysql
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    DB_POOL_SIZE: int = 5         # Connections to keep open
    DB_MAX_OVERFLOW: int = 10     # Burst connections
    DB_POOL_RECYCLE: int = 3600   # Recycle connections every hour

    model_config = SettingsConfigDict(
        env_file=".env", 
        case_sensitive=True,
        extra="ignore"
    )

    @computed_field(return_type=str)
    @property
    def DB_URL(self):
        match self.DB_MANAGER:
            case "mysql":
                return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            case _:
                return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()