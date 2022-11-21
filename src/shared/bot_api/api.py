from __future__ import annotations

from datetime import datetime
from functools import lru_cache
from typing import List

import attr
from src.shared.bot_api.models import FixtureCollection
from src.shared.bot_api.models import Participant
from src.shared.db_api.api import DbApi
from src.shared.db_api.api import get_db_api
from src.shared.open_weather_map_api.api import get_open_weather_map_api
from src.shared.open_weather_map_api.api import OpenWeatherMapApi
from src.shared.telegram_api.api import get_telegram_api
from src.shared.telegram_api.api import TelegramApi


@lru_cache
def get_bot_api() -> BotApi:
    return BotApi()


@attr.s
class BotApi:
    db_api: DbApi = attr.ib(factory=get_db_api)
    telegram_api: TelegramApi = attr.ib(factory=get_telegram_api)
    open_weather_map_api: OpenWeatherMapApi = attr.ib(factory=get_open_weather_map_api)

    @property
    def weather_message(self) -> str:
        if datetime.utcnow().hour <= 12:
            time_of_day = "Morning"
        elif datetime.utcnow().hour <= 18:
            time_of_day = "Afternoon"
        else:
            time_of_day = "Evening"
        weather_emoji = self.open_weather_map_api.get_weather_in_peckham()
        return f"{weather_emoji} Good {time_of_day} Friends {weather_emoji}"

    @property
    def good_luck_message(self) -> str:
        return "🍀 Good luck everyone! 🍀"

    def generate_morning_message(self) -> None:
        fixture_collection = self.get_fixtures_today()
        step_one_messages_to_send = [
            self.weather_message,
            fixture_collection.fixture_message,
        ]
        step_two_messages_to_send = [f.morning_message for f in self.get_fixtures_today()]
        if step_two_messages_to_send:
            step_three_messages_to_send = [self.good_luck_message]
        else:
            step_three_messages_to_send = []
        all_messages_to_send = step_one_messages_to_send + step_two_messages_to_send + step_three_messages_to_send

        for message in all_messages_to_send:
            self.telegram_api.send_message(message)

    def get_fixtures_today(self) -> FixtureCollection:
        return FixtureCollection.from_fixtures(self.db_api.get_fixtures(today_only=True))

    def get_participants(self) -> List[Participant]:
        return [Participant.from_orm(p) for p in self.db_api.get_participants()]

    # def get_teams(self) -> List[Team]:
    #     return [Team.from_orm(t) for t in session.query(TeamORM).all()]
    #
    # def get_fixtures(self, today: bool = True) -> List[Fixture]:
    #     with self.session as session:
    #         if today:
    #             query = (
    #                 session.query(FixtureORM)
    #                 .filter(
    #                     func.extract("month", FixtureORM.kick_off) == datetime.today().month,
    #                     func.extract("year", FixtureORM.kick_off) == datetime.today().year,
    #                     func.extract("day", FixtureORM.kick_off) == datetime.today().day,
    #                 )
    #                 .order_by(FixtureORM.kick_off)
    #             )
    #         else:
    #             query = session.query(FixtureORM)
    #         return [Fixture.from_orm(f) for f in query.order_by(FixtureORM.kick_off).all()]
