from __future__ import annotations
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from src.shared.telegram_api.models import TelegramUser
from src.shared.football_api.models import FootballTeam

Base = declarative_base()


class Participant(Base):
    __tablename__ = "participant"

    id: int = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name: str = Column(String, nullable=False)
    telegram_id: int = Column(Integer, nullable=False)

    team = relationship("TeamParticipantAssociation", back_populates="team")

    @classmethod
    def from_telegram_user(cls, telegram_user: TelegramUser) -> Participant:
        return cls(name=telegram_user.first_name, telegram_id=telegram_user.id)


class Team(Base):
    __tablename__ = "team"

    id: int = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)

    participant = relationship("TeamParticipantAssociation", back_populates="participant")

    @classmethod
    def from_football_team(cls, football_team: FootballTeam) -> Team:
        return cls(name=football_team.name)


class TeamParticipantAssociation(Base):
    __tablename__ = "team_participant_association"

    id: int = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    team_id = Column(Integer, ForeignKey("team.id"), nullable=False)
    participant_id = Column(Integer, ForeignKey("participant.id"), nullable=False)

    team = relationship("Team", back_populates="participant")
    participant = relationship("Participant", back_populates="team")
