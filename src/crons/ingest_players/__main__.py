from loguru import logger
from src.shared.bot_api.api import BotApiError
from src.shared.bot_api.api import get_bot_api
from src.shared.football_api.api import get_football_api


def main() -> None:
    logger.info("running ingest_players")

    bot_api = get_bot_api()

    for player in get_football_api().get_all_players():
        try:
            bot_api.save_or_update_player(player)
        except BotApiError:
            pass


if __name__ == "__main__":
    main()
