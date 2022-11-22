from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel
from src.shared.open_weather_map_api.responses import WeatherResponse

WEATHER_ID_TO_EMOJI = {
    200: "🌩",
    201: "⛈️",
    202: "⛈",
    210: "🌩",
    211: "🌩",
    212: "🌩",
    221: "🌩",
    230: "🌩",
    231: "🌩",
    232: "⛈",
    300: "🌧",
    301: "🌧",
    302: "🌧",
    310: "🌧",
    311: "🌧",
    312: "🌧",
    313: "🌧",
    314: "🌧",
    321: "🌧",
    500: "🌧",
    501: "🌧",
    502: "🌧",
    503: "🌧",
    504: "🌧",
    511: "🌧",
    520: "🌧",
    521: "🌧",
    522: "🌧",
    531: "🌧",
    600: "🌨",
    601: "🌨",
    602: "🌨",
    611: "🌨",
    612: "🌨",
    613: "🌨",
    615: "🌨",
    616: "🌨",
    620: "🌨",
    621: "🌨",
    622: "🌨",
    701: "🌁",
    711: "🌁",
    721: "🌁",
    731: "🌁",
    741: "🌁",
    751: "🌁",
    761: "🌁",
    762: "🌁",
    771: "🌁",
    781: "🌁",
    800: "☀️",
    801: "🌤",
    802: "⛅",
    803: "🌥",
    804: "☁️",
}


class Weather(BaseModel):
    emoji: str

    @classmethod
    def from_response(cls, response: WeatherResponse) -> Weather:
        return cls(emoji=WEATHER_ID_TO_EMOJI[response["weather"][0]["id"]])

    @property
    def weather_message(self) -> str:
        if datetime.utcnow().hour <= 12:
            time_of_day = "Morning"
        elif datetime.utcnow().hour <= 18:
            time_of_day = "Afternoon"
        else:
            time_of_day = "Evening"
        weather_emoji = self.emoji
        return f"{weather_emoji} Good {time_of_day} Friends {weather_emoji}"
