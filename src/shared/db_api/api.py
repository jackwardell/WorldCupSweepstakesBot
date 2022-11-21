from __future__ import annotations

from datetime import datetime
from functools import lru_cache
from typing import List

import attr
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from src.shared.config import get_config
from src.shared.db_api.models import FixtureORM
from src.shared.db_api.models import ParticipantORM
from src.shared.db_api.models import TeamAndParticipantORM
from src.shared.db_api.models import TeamORM
from src.shared.football_api.models import FootballFixture
from src.shared.football_api.models import FootballTeam
from src.shared.telegram_api.models import TelegramUser

engine = create_engine(get_config().SQLALCHEMY_URL)


@lru_cache
def get_db_api() -> DbApi:
    return DbApi()


@attr.s
class DbApi:
    session: Session = attr.ib(factory=lambda: Session(engine))

    def get_participants(self) -> List[ParticipantORM]:
        with self.session as session:
            return session.query(ParticipantORM).all()

    def save_participant(self, telegram_user: TelegramUser) -> ParticipantORM:
        with self.session as session:
            participant = ParticipantORM.from_telegram_user(telegram_user)
            session.add(participant)
            session.commit()
            return participant

    def get_teams(self) -> List[TeamORM]:
        with self.session as session:
            return session.query(TeamORM).all()

    def save_team(self, football_team: FootballTeam) -> TeamORM:
        with self.session as session:
            team = TeamORM.from_football_team(football_team)
            session.add(team)
            session.commit()
            return team

    def get_teams_and_participants(self) -> List[TeamAndParticipantORM]:
        with self.session as session:
            return session.query(TeamAndParticipantORM).all()

    def save_team_and_participant(self, team_name: str, participant_name: str) -> TeamAndParticipantORM:
        with self.session as session:
            team_and_participant = TeamAndParticipantORM(team_name=team_name, participant_name=participant_name)
            session.add(team_and_participant)
            session.commit()
            return team_and_participant

    def get_fixtures(self, today_only: bool = True) -> List[FixtureORM]:
        with self.session as session:
            if today_only:
                query = (
                    session.query(FixtureORM)
                    .filter(func.extract("month", FixtureORM.kick_off) == datetime.today().month)
                    .filter(func.extract("year", FixtureORM.kick_off) == datetime.today().year)
                    .filter(func.extract("day", FixtureORM.kick_off) == datetime.today().day)
                    .order_by(FixtureORM.kick_off)
                )
            else:
                query = session.query(FixtureORM)
            return query.all()

    def save_or_update_fixtures(self, football_fixture: FootballFixture) -> FixtureORM:
        with self.session as session:
            try:
                fixture = (
                    session.query(FixtureORM)
                    .filter(FixtureORM.home_team_name == football_fixture.home_team_name)
                    .filter(FixtureORM.away_team_name == football_fixture.away_team_name)
                    .filter(FixtureORM.kick_off == football_fixture.kick_off)
                    .filter(FixtureORM.round == football_fixture.round)
                    .one()
                )
                if fixture.home_team_goals is not None:
                    fixture.home_team_goals = football_fixture.home_team_goals
                if fixture.away_team_goals is not None:
                    fixture.away_team_goals = football_fixture.away_team_goals
                if fixture.home_team_won is not None:
                    fixture.home_team_won = football_fixture.home_team_winner
                if fixture.away_team_won is not None:
                    fixture.away_team_won = football_fixture.away_team_winner
                session.commit()
            except NoResultFound:
                fixture = FixtureORM.from_football_fixture(football_fixture)
                session.add(fixture)
                session.commit()
            return fixture
