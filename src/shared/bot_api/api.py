from __future__ import annotations

from datetime import datetime
from functools import lru_cache
from typing import List

import attr
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from src.shared.bot_api.db import FixtureORM
from src.shared.bot_api.db import ParticipantORM
from src.shared.bot_api.db import TeamAndParticipantORM
from src.shared.bot_api.db import TeamORM
from src.shared.bot_api.models import Fixture
from src.shared.bot_api.models import Participant
from src.shared.bot_api.models import Team
from src.shared.bot_api.models import TeamAndParticipant
from src.shared.config import get_config
from src.shared.football_api.models import FootballFixture
from src.shared.football_api.models import FootballTeam
from src.shared.open_weather_map_api.api import get_open_weather_map_api
from src.shared.open_weather_map_api.api import OpenWeatherMapApi
from src.shared.telegram_api.api import get_telegram_api
from src.shared.telegram_api.api import TelegramApi
from src.shared.telegram_api.models import TelegramUser

engine = create_engine(get_config().SQLALCHEMY_URL)


class BotApiError(Exception):
    pass


@lru_cache
def get_bot_api() -> BotApi:
    return BotApi()


@attr.s
class BotApi:
    session: Session = attr.ib(factory=lambda: Session(engine))
    telegram_api: TelegramApi = attr.ib(factory=get_telegram_api)
    open_weather_map_api: OpenWeatherMapApi = attr.ib(factory=get_open_weather_map_api)

    def get_number_of_fixtures_morning_message(self) -> str:
        fixtures = self.get_fixtures()
        if len(fixtures) == 0:
            return "No fixtures today, just chill the fuck out 🍻"
        elif len(fixtures) == 1:
            return "Today there is one match. Here's the fixture 👇"
        else:
            return f"Today there {len(fixtures)} matches. Here are the fixtures 👇"

    def get_participants(self) -> List[Participant]:
        with self.session as session:
            return [Participant.from_orm(p) for p in session.query(ParticipantORM).all()]

    def save_participant(self, telegram_user: TelegramUser) -> Participant:
        with self.session as session:
            participant = ParticipantORM.from_telegram_user(telegram_user)
            session.add(participant)
            try:
                session.commit()
                return Participant.from_orm(participant)
            except IntegrityError as e:
                session.rollback()
                raise BotApiError(e) from e

    def get_teams(self) -> List[Team]:
        with self.session as session:
            return [Team.from_orm(t) for t in session.query(TeamORM).all()]

    def save_team(self, football_team: FootballTeam) -> Team:
        with self.session as session:
            team = TeamORM.from_football_team(football_team)
            session.add(team)
            try:
                session.commit()
                return Team.from_orm(team)
            except IntegrityError as e:
                session.rollback()
                raise BotApiError(e) from e

    def get_teams_and_participants(self) -> List[TeamAndParticipant]:
        with self.session as session:
            return [TeamAndParticipant.from_orm(t) for t in session.query(TeamAndParticipantORM).all()]

    def save_team_and_participant(self, team_name: str, participant_name: str) -> TeamAndParticipant:
        with self.session as session:
            team_and_participant = TeamAndParticipantORM.from_team_name_and_participant_name(
                team_name=team_name,
                participant_name=participant_name,
            )
            session.add(team_and_participant)
            try:
                session.commit()
                return TeamAndParticipant.from_orm(team_and_participant)
            except IntegrityError as e:
                session.rollback()
                raise BotApiError(e) from e

    def get_fixtures(self, today_only: bool = True) -> List[Fixture]:
        with self.session as session:
            if today_only:
                query = (
                    session.query(FixtureORM)
                    .filter(func.extract("month", FixtureORM.kick_off) == datetime.today().month)
                    .filter(func.extract("year", FixtureORM.kick_off) == datetime.today().year)
                    .filter(func.extract("day", FixtureORM.kick_off) == datetime.today().day)
                    .order_by(FixtureORM.kick_off)
                    .all()
                )
            else:
                query = session.query(FixtureORM).all()
            return [Fixture.from_orm(f) for f in query]

    def save_or_update_fixture(self, football_fixture: FootballFixture) -> Fixture:
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
                fixture.home_team_goals = football_fixture.home_team_goals
                fixture.away_team_goals = football_fixture.away_team_goals
                fixture.home_team_won = football_fixture.home_team_winner
                fixture.away_team_won = football_fixture.away_team_winner
                session.add(fixture)
                session.commit()
            except NoResultFound:
                session.rollback()
                fixture = FixtureORM.from_football_fixture(football_fixture)
                session.add(fixture)
                session.commit()
            return Fixture.from_orm(fixture)
