from src.shared.db.api import get_db_api
from src.shared.football_api.api import get_football_api

if __name__ == "__main__":
    football_api = get_football_api()
    db_api = get_db_api()

    teams = get_football_api().get_teams()

    for team in teams:
        db_api.save_team(team)
