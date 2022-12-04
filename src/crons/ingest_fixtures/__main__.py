from loguru import logger
from src.shared.bot_api.api import BotApiError
from src.shared.bot_api.api import get_bot_api
from src.shared.football_api.api import get_football_api


def main() -> None:
    logger.info("running ingest_fixtures")

    bot_api = get_bot_api()

    for fixture in get_football_api().get_fixtures(today_only=False):
        try:
            bot_api.save_or_update_fixture(fixture)
        except BotApiError:
            pass


if __name__ == "__main__":
    main()
