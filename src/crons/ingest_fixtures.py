from src.shared.db.api import get_db_api
from src.shared.football_api.api import get_football_api

if __name__ == "__main__":
    db_api = get_db_api()

    for fixture in get_football_api().get_fixtures(today_only=False):
        db_api.save_or_update_fixtures(fixture)
