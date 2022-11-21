from __future__ import annotations

from functools import lru_cache
from typing import List

import attr
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.shared.config import get_config
from src.shared.db.models import ParticipantORM
from src.shared.db.models import TeamAndParticipantORM
from src.shared.db.models import TeamORM
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

    def save_team_and_participant(self, team_name: str, participant_name: str) -> TeamAndParticipantORM:
        with self.session as session:
            team_and_participant = TeamAndParticipantORM(team_name=team_name, participant_name=participant_name)
            session.add(team_and_participant)
            session.commit()
            return team_and_participant
