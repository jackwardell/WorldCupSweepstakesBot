from src.shared.football_api.api import get_football_api
from src.shared.db.api import get_session
from src.shared.db.models import FixtureORM

if __name__ == "__main__":
    bot_api = get_football_api()

    football_fixtures = get_football_api().get_fixtures(today_only=False)

    with get_session() as session:
        for football_fixture in football_fixtures:
            participant = FixtureORM.from_telegram_user(user)
            session.add(participant)

        session.commit()
