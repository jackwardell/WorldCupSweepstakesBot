from src.shared.bot_api.api import BotApiError
from src.shared.bot_api.api import get_bot_api
from src.shared.telegram_api.api import get_telegram_api


def main() -> None:
    bot_api = get_bot_api()

    for user in get_telegram_api().get_users():
        try:
            bot_api.save_participant(user)
        except BotApiError:
            pass


if __name__ == "__main__":
    main()
