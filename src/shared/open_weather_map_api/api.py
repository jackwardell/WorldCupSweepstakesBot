import attr
import requests
from src.shared.config import get_config

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"




@attr.s
class OpenWeatherMapApi:
    api_key = attr.ib(factory=lambda: get_config().OPEN_WEATHER_MAP_API_KEY)

    def get_weather_in_peckham(self) -> str:
        weather_id = requests.get(
            WEATHER_URL,
            params={
                "q": "Peckham",
                "appid": self.api_key
            }
        ).json()
        # ["weather"][0]["id"]
        from pprint import pprint
        pprint(weather_id)


OpenWeatherMapApi().get_weather_in_peckham()