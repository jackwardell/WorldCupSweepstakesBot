from __future__ import annotations
from typing import List

import attr
from sqlalchemy.orm import Session

from src.shared.bot.models import Participant, Team
from src.shared.db.api import get_session
from src.shared.db.models import ParticipantORM, TeamORM
from src.shared.football_api.api import FootballApi
from src.shared.football_api.api import get_football_api
from src.shared.open_weather_map_api.api import OpenWeatherMapApi
from src.shared.open_weather_map_api.api import get_open_weather_map_api
from src.shared.telegram_api.api import TelegramApi
from src.shared.telegram_api.api import get_telegram_api

from functools import lru_cache


@lru_cache
def get_bot_api() -> BotApi:
    return BotApi()


@attr.s
class BotApi:
    telegram_api: TelegramApi = attr.ib(factory=get_telegram_api)
    football_api: FootballApi = attr.ib(factory=get_football_api)
    get_open_weather_map_api: OpenWeatherMapApi = attr.ib(factory=get_open_weather_map_api)
    session: Session = attr.ib(factory=get_session)

    def get_participants(self) -> List[Participant]:
        with self.session as session:
            return [Participant.from_orm(p) for p in session.query(ParticipantORM).all()]

    def get_teams(self) -> List[Team]:
        with self.session as session:
            return [Team.from_orm(t) for t in session.query(TeamORM).all()]
