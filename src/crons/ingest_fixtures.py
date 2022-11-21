from src.shared.football_api.api import get_football_api
from src.shared.db.api import get_session
from src.shared.db.models import FixtureORM
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime

if __name__ == "__main__":
    bot_api = get_football_api()

    football_fixtures = get_football_api().get_fixtures(today_only=False)

    with get_session() as session:
        for football_fixture in football_fixtures:
            try:
                existing_fixture = (
                    session.query(FixtureORM)
                    .filter(FixtureORM.home_team_name == football_fixture.home_team_name)
                    .filter(FixtureORM.away_team_name == football_fixture.away_team_name)
                    .filter(FixtureORM.kick_off == football_fixture.kick_off)
                    .filter(FixtureORM.round == football_fixture.round)
                    .one()
                )
                if existing_fixture.home_team_goals is not None:
                    existing_fixture.home_team_goals = football_fixture.home_team_goals
                if existing_fixture.away_team_goals is not None:
                    existing_fixture.away_team_goals = football_fixture.away_team_goals
                if existing_fixture.home_team_won is not None:
                    existing_fixture.home_team_won = football_fixture.home_team_winner
                if existing_fixture.away_team_won is not None:
                    existing_fixture.away_team_won = football_fixture.away_team_winner
                session.commit()

            except NoResultFound:
                fixture = FixtureORM.from_football_fixture(football_fixture)
                session.add(fixture)
                session.commit()
