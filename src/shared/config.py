from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Union

from dotenv import load_dotenv
from pydantic import BaseSettings

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

load_dotenv(PROJECT_ROOT / ".env")


def is_testing() -> bool:
    return os.environ["TESTING"] == "true"


@lru_cache
def get_config() -> Union[TestConfig, ProdConfig]:
    return TestConfig() if is_testing() else ProdConfig()


class Config(BaseSettings):
    RAPID_API_KEY: str
    TELEGRAM_CHAT_ID: str
    TELEGRAM_API_KEY: str
    OPEN_WEATHER_MAP_API_KEY: str
    SQLALCHEMY_URL: str


class TestConfig(BaseSettings):
    RAPID_API_KEY = "test1"
    TELEGRAM_CHAT_ID = "test2"
    TELEGRAM_API_KEY = "test3"
    OPEN_WEATHER_MAP_API_KEY = "test4"
    SQLALCHEMY_URL = "sqlite:///test5"


class ProdConfig(BaseSettings):
    pass
