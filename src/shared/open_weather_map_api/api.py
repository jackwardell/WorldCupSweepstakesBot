from __future__ import annotations

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
