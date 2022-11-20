from src.shared.telegram_api.api import get_telegram_api
from src.shared.db.api import get_session

if __name__ == "__main__":
    telegram_api = get_telegram_api()
    session = get_session()

    users = get_telegram_api().get_users()
    for user in users:
