from src.shared.bot_api.api import get_bot_api
from src.shared.open_weather_map_api.api import get_open_weather_map_api
from src.shared.telegram_api.api import get_telegram_api

if __name__ == "__main__":
    telegram_api = get_telegram_api()
    weather_api = get_open_weather_map_api()
    bot_api = get_bot_api()

    weather_emoji = weather_api.get_weather_in_peckham().emoji
    good_morning_message = f"{weather_emoji} Good Evening Friends {weather_emoji}"
    telegram_api.send_message(good_morning_message)

    for fixture in get_bot_api().get_fixtures():
        telegram_api.send_message(fixture.evening_message)

        # telegram_api.send_message(fixture.evening_message)
        # if fixture.home_and_away_rivals_equal:
        #     matching_rivals_message_ids.append((fixture.home_rival, message_id))

    # if matching_rivals_message_ids:
    #     for c, (participant, matching_rivals_message_id) in enumerate(matching_rivals_message_ids):
    #         telegram_api.send_message(MATCHING_RIVALS_COMMENTS[c], reply_to_message_id=matching_rivals_message_id)
    #         telegram_api.send_spider_man_image(participant)
