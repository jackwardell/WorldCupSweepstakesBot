from __future__ import annotations

from functools import lru_cache

from pydantic import BaseSettings


class Config(BaseSettings):
    RAPID_API_KEY: str
    TELEGRAM_CHAT_ID: str
    TELEGRAM_API_KEY: str
    OPEN_WEATHER_MAP_API_KEY: str


@lru_cache
def get_config() -> Config:
    return Config()
