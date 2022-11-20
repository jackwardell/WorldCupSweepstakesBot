from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

load_dotenv(PROJECT_ROOT / ".env")


@lru_cache
def get_config() -> Config:
    return Config()


class Config(BaseSettings):
    RAPID_API_KEY: str
    TELEGRAM_CHAT_ID: str
    TELEGRAM_API_KEY: str
    OPEN_WEATHER_MAP_API_KEY: str
    SQLALCHEMY_URL: str
