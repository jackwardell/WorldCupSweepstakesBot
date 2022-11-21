from src.shared.db.api import get_db_api
from src.shared.telegram_api.api import get_telegram_api

if __name__ == "__main__":
    telegram_api = get_telegram_api()
    db_api = get_db_api()

    users = get_telegram_api().get_users()

    for user in users:
        db_api.save_participant(user)
