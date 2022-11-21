from src.shared.db_api.api import DbApiError
from src.shared.db_api.api import get_db_api
from src.shared.football_api.api import get_football_api


def main() -> None:
    db_api = get_db_api()

    for fixture in get_football_api().get_fixtures(today_only=False):
        try:
            db_api.save_or_update_fixture(fixture)
        except DbApiError:
            pass


if __name__ == "__main__":
    main()
