from __future__ import annotations

from datetime import datetime
from functools import lru_cache
from typing import List

import attr
from sqlalchemy import func
from sqlalchemy.orm import Session
from src.shared.bot.models import Fixture
from src.shared.bot.models import Participant
from src.shared.bot.models import Team
from src.shared.db.api import get_session
from src.shared.db.models import FixtureORM
from src.shared.db.models import ParticipantORM
from src.shared.db.models import TeamORM
from src.shared.football_api.api import FootballApi
from src.shared.football_api.api import get_football_api
from src.shared.telegram_api.api import get_telegram_api
from src.shared.telegram_api.api import TelegramApi

# from src.shared.open_weather_map_api.api import (OpenWeatherMapApi,
#                                                  get_open_weather_map_api)


@lru_cache
def get_bot_api() -> BotApi:
    return BotApi()


@attr.s
class BotApi:
    telegram_api: TelegramApi = attr.ib(factory=get_telegram_api)
    football_api: FootballApi = attr.ib(factory=get_football_api)
    # get_open_weather_map_api: OpenWeatherMapApi = attr.ib(factory=get_open_weather_map_api)
    session: Session = attr.ib(factory=get_session)

    def get_participants(self) -> List[Participant]:
        with self.session as session:
            return [Participant.from_orm(p) for p in session.query(ParticipantORM).all()]

    def get_teams(self) -> List[Team]:
        with self.session as session:
            return [Team.from_orm(t) for t in session.query(TeamORM).all()]

    def get_fixtures(self, today: bool = True) -> List[Fixture]:
        with self.session as session:
            if today:
                query = (
                    session.query(FixtureORM)
                    .filter(
                        func.extract("month", FixtureORM.kick_off) == datetime.today().month,
                        func.extract("year", FixtureORM.kick_off) == datetime.today().year,
                        func.extract("day", FixtureORM.kick_off) == datetime.today().day,
                    )
                    .order_by(FixtureORM.kick_off)
                )
            else:
                query = session.query(FixtureORM)
            return [Fixture.from_orm(f) for f in query.order_by(FixtureORM.kick_off).all()]
