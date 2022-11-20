from __future__ import annotations
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from src.shared.telegram_api.models import TelegramUser
Base = declarative_base()


class Participant(Base):
    __tablename__ = "participant"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String)
    telegram_id: int = Column(Integer)

    @classmethod
    def from_telegram_user(cls, telegram_user: TelegramUser) -> Participant:
        return cls(name=telegram_user.first_name, telegram_id=telegram_user.id)


class Team(Base):
    __tablename__ = "team"

    name = Column(String, primary_key=True)
    emoji = Column(String)


# class ParticipantTeamAssociation(Base):
#     __tablename__ = "participant_team_association"
#
#     team_name =
