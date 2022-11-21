from src.shared.db.api import get_db_api
from src.shared.football_api.api import get_football_api

if __name__ == "__main__":
    db_api = get_db_api()

    for team in get_football_api().get_teams():
        db_api.save_team(team)
