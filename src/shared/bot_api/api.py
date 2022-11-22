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

    # @property
    # def weather_message(self) -> str:
    #     if datetime.utcnow().hour <= 12:
    #         time_of_day = "Morning"
    #     elif datetime.utcnow().hour <= 18:
    #         time_of_day = "Afternoon"
    #     else:
    #         time_of_day = "Evening"
    #     weather_emoji = self.open_weather_map_api.get_weather_in_peckham()
    #     return f"{weather_emoji} Good {time_of_day} Friends {weather_emoji}"
    #
    # @property
    # def good_luck_message(self) -> str:
    #     return "🍀 Good luck everyone! 🍀"
    #
    # def generate_morning_message(self) -> None:
    #     fixture_collection = self.get_fixtures_today()
    #     step_one_messages_to_send = [
    #         self.weather_message,
    #         fixture_collection.fixture_message,
    #     ]
    #     step_two_messages_to_send = [f.morning_message for f in self.get_fixtures_today()]
    #     if step_two_messages_to_send:
    #         step_three_messages_to_send = [self.good_luck_message]
    #     else:
    #         step_three_messages_to_send = []
    #     all_messages_to_send = step_one_messages_to_send + step_two_messages_to_send + step_three_messages_to_send
    #
    #     for message in all_messages_to_send:
    #         self.telegram_api.send_message(message)

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
                session.rollback()
                fixture = FixtureORM.from_football_fixture(football_fixture)
                session.add(fixture)
                session.commit()
            return Fixture.from_orm(fixture)
