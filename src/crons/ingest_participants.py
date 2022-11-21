from src.shared.db_api.api import DbApiError
from src.shared.db_api.api import get_db_api
from src.shared.telegram_api.api import get_telegram_api


def main() -> None:
    db_api = get_db_api()

    for user in get_telegram_api().get_users():
        try:
            db_api.save_participant(user)
        except DbApiError:
            pass


if __name__ == "__main__":
    main()
