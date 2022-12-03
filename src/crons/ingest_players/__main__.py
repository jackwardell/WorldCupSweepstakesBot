import json

from src.shared.bot_api.api import BotApiError
from src.shared.bot_api.api import get_bot_api
from src.shared.config import PROJECT_ROOT
from src.shared.football_api.api import get_football_api


def main() -> None:
    bot_api = get_bot_api()

    for player in get_football_api().get_all_players():
        try:
            bot_api.save_player(player)
        except BotApiError:
            pass

    with open(PROJECT_ROOT / "src" / "assets" / "players.json", mode="w+") as file:
        file.write(json.dumps(bot_api.get_players()))


if __name__ == "__main__":
    main()
