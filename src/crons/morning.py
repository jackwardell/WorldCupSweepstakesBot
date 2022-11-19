from src.shared.rapid_api.api import get_football_api
from src.shared.telegram_api.api import get_telegram_api

if __name__ == "__main__":
    football_api = get_football_api()
    # telegram_bot = get_telegram_bot()

    fixtures = football_api.get_fixtures()

    for fixture in fixtures:
        print(fixture.morning_message)
