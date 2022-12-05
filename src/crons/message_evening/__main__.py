from time import sleep

from src.shared.bot_api.api import get_bot_api
from src.shared.open_weather_map_api.api import get_open_weather_map_api
from src.shared.telegram_api.api import get_telegram_api


def main() -> None:
    telegram_api = get_telegram_api()
    weather_api = get_open_weather_map_api()
    bot_api = get_bot_api()

    fixtures = bot_api.get_fixtures()
    if fixtures:
        telegram_api.send_message(weather_api.get_weather_in_peckham().weather_message)
        sleep(1)
        telegram_api.send_message("Here are the results from today 👇")
        sleep(1)

        its_coming_home = []
        youre_out = {}
        for fixture in fixtures:
            msg_id = telegram_api.send_message(fixture.evening_message)
            youre_out[msg_id] = fixture
            if (fixture.home_team.name == "England" and fixture.home_team_winner) or (
                fixture.away_team.name == "England" and fixture.away_team_winner
            ):
                its_coming_home.append(msg_id)
            sleep(1)

        if its_coming_home:
            telegram_api.send_its_coming_home_image(its_coming_home.pop())

        for msg_id, fixture in youre_out.items():
            sleep(1)
            telegram_api.send_message(
                f"☠️ Oh btw {fixture.loser_participant.telegram_tag}, "
                f"{fixture.loser_team.name_and_emoji} is out, get rekt you fucking loser ☠️",
                reply_to_message_id=msg_id,
            )


if __name__ == "__main__":
    main()
