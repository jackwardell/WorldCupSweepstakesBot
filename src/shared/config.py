from __future__ import annotations

from functools import lru_cache

from pydantic import BaseSettings
from dotenv import load_dotenv
from src.shared.static import PROJECT_ROOT

load_dotenv(PROJECT_ROOT / ".env")


class Config(BaseSettings):
    RAPID_API_KEY: str
    TELEGRAM_CHAT_ID: str
    TELEGRAM_API_KEY: str
    OPEN_WEATHER_MAP_API_KEY: str
    FERNET_ENCRYPTION_KEY: str
    SQLALCHEMY_URL: str


@lru_cache
def get_config() -> Config:
    return Config()
