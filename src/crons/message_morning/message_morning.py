from time import sleep

from src.shared.bot_api.api import get_bot_api
from src.shared.open_weather_map_api.api import get_open_weather_map_api
from src.shared.telegram_api.api import get_telegram_api


def main() -> None:
    telegram_api = get_telegram_api()
    weather_api = get_open_weather_map_api()
    bot_api = get_bot_api()

    telegram_api.send_message(weather_api.get_weather_in_peckham().weather_message)
    telegram_api.send_message(bot_api.get_number_of_fixtures_morning_message())
    sleep(1)

    fixtures = bot_api.get_fixtures()

    matching_participants_and_message_ids = {}

    if fixtures:
        for fixture in fixtures:
            message_id = telegram_api.send_message(fixture.morning_message)
            sleep(1)
            if fixture.matching_participants:
                matching_participants_and_message_ids[fixture.home_participant.name] = message_id

        telegram_api.send_message("🍀 Good luck everyone! 🍀")
        sleep(1)

    if matching_participants_and_message_ids:
        for participant_name, message_id in matching_participants_and_message_ids.items():
            telegram_api.send_spiderman_image(participant_name, reply_to_message_id=message_id)
            sleep(1)


if __name__ == "__main__":
    main()
