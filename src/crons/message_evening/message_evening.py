from time import sleep

from src.shared.bot_api.api import get_bot_api
from src.shared.open_weather_map_api.api import get_open_weather_map_api
from src.shared.telegram_api.api import get_telegram_api


def main() -> None:
    telegram_api = get_telegram_api()
    weather_api = get_open_weather_map_api()
    bot_api = get_bot_api()

    telegram_api.send_message(weather_api.get_weather_in_peckham().weather_message)
    sleep(1)

    fixtures = bot_api.get_fixtures()
    if fixtures:
        telegram_api.send_message("Here are the results from today 👇")
        sleep(1)

        for fixture in fixtures:
            telegram_api.send_message(fixture.evening_message)
            sleep(1)


if __name__ == "__main__":
    main()
