from src.shared.football_api.api import get_football_api
from src.shared.db.api import get_session
from src.shared.db.models import TeamORM

if __name__ == "__main__":
    football_api = get_football_api()

    teams = get_football_api().get_teams()

    with get_session() as session:
        for team in teams:
            participant = TeamORM.from_football_team(team)
            session.add(participant)

        session.commit()
