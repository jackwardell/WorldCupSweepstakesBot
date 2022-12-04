import time

from loguru import logger
from src.shared.bot_api.api import BotApiError
from src.shared.bot_api.api import get_bot_api
from src.shared.football_api.api import get_football_api


def main() -> None:
    logger.info("running ingest_fixture_events")

    bot_api = get_bot_api()
    football_api = get_football_api()

    for fixture in get_bot_api().get_fixtures(today_only=False):
        try:
            fixture_events = football_api.get_fixture_events(fixture.football_api_id)
            for fixture_event in fixture_events:
                bot_api.save_fixture_event(fixture_event)
        except BotApiError:
            pass
        time.sleep(2)


if __name__ == "__main__":
    main()
