from __future__ import annotations

from datetime import datetime
from functools import lru_cache

import attr
import requests
from src.shared.config import get_config
from src.shared.open_weather_map_api.domain import Weather

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


@lru_cache
def get_open_weather_map_api() -> OpenWeatherMapApi:
    return OpenWeatherMapApi()


@attr.s
class OpenWeatherMapApi:
    api_key: str = attr.ib(factory=lambda: get_config().OPEN_WEATHER_MAP_API_KEY)

    def get_weather_in_peckham(self) -> Weather:
        response = requests.get(WEATHER_URL, params={"q": "Peckham", "appid": self.api_key})
        return Weather.from_response(response.json())

    def get_weather_message(self) -> str:
        if datetime.utcnow().hour <= 12:
            time_of_day = "Morning"
        elif datetime.utcnow().hour <= 18:
            time_of_day = "Afternoon"
        else:
            time_of_day = "Evening"
        weather_emoji = self.get_weather_in_peckham()
        return f"{weather_emoji} Good {time_of_day} Friends {weather_emoji}"
