from src.shared.football_api.api import get_football_api
from src.shared.db.api import get_session
from src.shared.db.models import Participant

if __name__ == "__main__":
    football_api = get_football_api()

    teams = get_football_api().get_teams()

    with get_session() as session:
        for team in teams:
            participant = Participant.from_telegram_user(user)
            session.add(participant)

        session.commit()
