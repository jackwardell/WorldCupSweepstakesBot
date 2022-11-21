from __future__ import annotations

from functools import lru_cache
from typing import List

import attr
from src.shared.bot_api.models import Participant
from src.shared.db_api.api import DbApi
from src.shared.db_api.api import get_db_api


@lru_cache
def get_bot_api() -> BotApi:
    return BotApi()


@attr.s
class BotApi:
    db_api: DbApi = attr.ib(factory=get_db_api)

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
