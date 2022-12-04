from __future__ import annotations

from datetime import datetime
from functools import lru_cache
from typing import List

import attr
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from src.shared.bot_api.db import DrawMappingORM
from src.shared.bot_api.db import FixtureEventORM
from src.shared.bot_api.db import FixtureORM
from src.shared.bot_api.db import ParticipantORM
from src.shared.bot_api.db import PlayerORM
from src.shared.bot_api.db import SweepstakeCategoryORM
from src.shared.bot_api.db import TeamORM
from src.shared.bot_api.models import Fixture
from src.shared.bot_api.models import Participant
from src.shared.bot_api.models import Player
from src.shared.bot_api.models import Team
from src.shared.config import get_config
from src.shared.football_api.models import FootballFixture
from src.shared.football_api.models import FootballFixtureEvent
from src.shared.football_api.models import FootballPlayer
from src.shared.football_api.models import FootballTeam
from src.shared.open_weather_map_api.api import get_open_weather_map_api
from src.shared.open_weather_map_api.api import OpenWeatherMapApi
from src.shared.schemas import SweepstakeCategoryEnum
from src.shared.telegram_api.api import get_telegram_api
from src.shared.telegram_api.api import TelegramApi
from src.shared.telegram_api.models import TelegramParticipant


class BotApiError(Exception):
    pass


@lru_cache
def get_engine() -> Engine:
    return create_engine(get_config().POSTGRES_DSN)


@lru_cache
def get_bot_api() -> BotApi:
    return BotApi()


@attr.s
class BotApi:
    session: Session = attr.ib(factory=lambda: Session(get_engine()))
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

    def save_participant(self, telegram_user: TelegramParticipant) -> Participant:
        logger.info(f"saving participant: {telegram_user.telegram_user_id}")
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

    def get_team(self, football_api_id: int) -> Team:
        with self.session as session:
            return Team.from_orm(session.query(TeamORM).filter(TeamORM.football_api_id == football_api_id).one())

    def save_team(self, football_team: FootballTeam) -> Team:
        logger.info(f"saving team: {football_team.football_api_id} {football_team.name}")
        with self.session as session:
            team = TeamORM.from_football_team(football_team)
            session.add(team)
            try:
                session.commit()
                return Team.from_orm(team)
            except IntegrityError as e:
                session.rollback()
                raise BotApiError(e) from e

    def save_team_drawn_by_participant(self, team_football_api_id: int, participant_telegram_user_id: int) -> None:
        logger.info(f"saving draw_mapping:  {team_football_api_id} drawn by {participant_telegram_user_id}")
        with self.session as session:
            team_drawn_by_participant = DrawMappingORM.from_team_football_api_id_and_participant_telegram_user_id(
                team_football_api_id=team_football_api_id,
                participant_telegram_user_id=participant_telegram_user_id,
            )
            session.add(team_drawn_by_participant)
            try:
                session.commit()
                return
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
        logger.info(f"saving or updating fixture: {football_fixture.football_api_id}")
        with self.session as session:
            try:
                fixture = (
                    session.query(FixtureORM)
                    .filter(FixtureORM.home_team_football_api_id == football_fixture.home_team_football_api_id)
                    .filter(FixtureORM.away_team_football_api_id == football_fixture.away_team_football_api_id)
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

    def save_sweepstake_category(
        self,
        sweepstake_category_enum: SweepstakeCategoryEnum,
        sweepstake_category_name: str,
        sweepstake_category_reward_amount: int,
    ) -> None:
        logger.info(f"saving sweepstake_category: {sweepstake_category_name} {sweepstake_category_name}")
        with self.session as session:
            session.add(
                SweepstakeCategoryORM(
                    id=sweepstake_category_enum.value,
                    name=sweepstake_category_name,
                    reward_amount=sweepstake_category_reward_amount,
                )
            )
            session.commit()

    def get_players(self) -> List[Player]:
        with self.session as session:
            return [Player.from_orm(p) for p in session.query(PlayerORM).all()]

    def save_player(self, football_player: FootballPlayer) -> None:
        logger.info(f"saving player: {football_player.football_api_id}")
        with self.session as session:
            try:
                session.add(PlayerORM.from_football_player(football_player))
                session.commit()
            except IntegrityError:
                session.rollback()

    def save_fixture_event(self, fixture_event: FootballFixtureEvent) -> None:
        logger.info(f"saving fixture_event: {fixture_event.fixture_football_api_id}")
        with self.session as session:
            try:
                session.add(FixtureEventORM.from_football_fixture_event(fixture_event))
                session.commit()
            except IntegrityError:
                session.rollback()
