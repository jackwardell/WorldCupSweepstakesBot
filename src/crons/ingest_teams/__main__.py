from loguru import logger
from src.shared.bot_api.api import BotApiError
from src.shared.bot_api.api import get_bot_api
from src.shared.football_api.api import get_football_api


def main() -> None:
    logger.info("running ingest_teams")

    bot_api = get_bot_api()

    for team in get_football_api().get_teams():
        try:
            bot_api.save_team(team)
        except BotApiError:
            pass


if __name__ == "__main__":
    main()
