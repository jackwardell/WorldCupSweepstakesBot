import attr
from src.shared.football_api.api import get_football_api, FootballApi
from src.shared.telegram_api.api import get_telegram_api, TelegramApi
from src.shared.open_weather_map_api.api import get_open_weather_map_api, OpenWeatherMapApi


@attr.s
class BotApp:
    telegram_api: TelegramApi = attr.ib(factory=get_telegram_api)
    football_api: FootballApi = attr.ib(factory=get_football_api)
    get_open_weather_map_api: OpenWeatherMapApi = attr.ib(factory=get_open_weather_map_api)
