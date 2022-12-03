from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def get_env_file() -> Path:
    return PROJECT_ROOT / ".env.test" if os.getenv("TESTING") == "true" else PROJECT_ROOT / ".env"


@lru_cache
def get_config() -> Config:
    load_dotenv(get_env_file())
    return Config()


class Config(BaseSettings):
    RAPID_API_KEY: str
    TELEGRAM_CHAT_ID: str
    TELEGRAM_API_KEY: str
    OPEN_WEATHER_MAP_API_KEY: str
    POSTGRES_DSN: str
