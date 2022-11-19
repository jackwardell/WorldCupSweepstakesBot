from src.shared.open_weather_map_api.api import get_open_weather_map_api
from src.shared.rapid_api.api import get_football_api
from src.shared.telegram_api.api import get_telegram_api

if __name__ == "__main__":
    football_api = get_football_api()
    telegram_api = get_telegram_api()
    weather_api = get_open_weather_map_api()

    weather_emoji = weather_api.get_weather_in_peckham().emoji
    good_morning_message = f'{weather_emoji} Good Morning Friends {weather_emoji}'
    telegram_api.send_message(good_morning_message)

    fixtures = football_api.get_fixtures()

    if fixtures:
        starting_message = f"Today there are {len(fixtures)} matches. Here are the fixtures today 👇"
        telegram_api.send_message(starting_message)
        for fixture in fixtures:
            print(fixture.morning_message)
            telegram_api.send_message(fixture.morning_message)
        ending_message = "🍀 Good luck everyone! 🍀"
        telegram_api.send_message(ending_message)

    else:
        starting_message = "No fixtures today, just chill the fuck out 🍻"
        telegram_api.send_message(starting_message)
