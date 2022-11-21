from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from src.shared.football_api.models import FootballFixture
from src.shared.football_api.models import FootballTeam
from src.shared.telegram_api.models import TelegramUser

Base = declarative_base()


class ParticipantORM(Base):
    __tablename__ = "participant"

    name: str = Column(String, primary_key=True, nullable=False)
    telegram_id: int = Column(BigInteger, nullable=False)

    team: TeamORM = relationship("TeamAndParticipantORM", back_populates="participant", uselist=False)

    @classmethod
    def from_telegram_user(cls, telegram_user: TelegramUser) -> ParticipantORM:
        return cls(name=telegram_user.first_name, telegram_id=telegram_user.id)


class TeamORM(Base):
    __tablename__ = "team"

    name: str = Column(String, primary_key=True, nullable=False)

    participant: ParticipantORM = relationship("TeamAndParticipantORM", back_populates="team", uselist=False)

    @classmethod
    def from_football_team(cls, football_team: FootballTeam) -> TeamORM:
        return cls(name=football_team.name)


class TeamAndParticipantORM(Base):
    __tablename__ = "team_and_participant"

    id: int = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    team_name: str = Column(String, ForeignKey("team.name"), nullable=False)
    participant_name: str = Column(String, ForeignKey("participant.name"), nullable=False)

    team: TeamORM = relationship("TeamORM", back_populates="participant", uselist=False)
    participant: ParticipantORM = relationship("ParticipantORM", back_populates="team", uselist=False)

    @classmethod
    def from_team_name_and_participant_name(cls, team_name: str, participant_name: str) -> TeamORM:
        return cls(team_name=team_name, participant_name=participant_name)


class FixtureORM(Base):
    __tablename__ = "fixture"

    id: int = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    home_team_name: str = Column(String, ForeignKey("team.name"), nullable=False)
    away_team_name: str = Column(String, ForeignKey("team.name"), nullable=False)
    home_team_goals: int = Column(Integer, nullable=True)
    away_team_goals: int = Column(Integer, nullable=True)
    home_team_won: bool = Column(Boolean, nullable=True)
    away_team_won: bool = Column(Boolean, nullable=True)
    venue_name: str = Column(String, nullable=False)
    venue_city: str = Column(String, nullable=False)
    kick_off: datetime = Column(DateTime, nullable=False)
    round: str = Column(String, nullable=False)

    home_team: TeamORM = relationship("TeamORM", foreign_keys="FixtureORM.home_team_name")
    away_team: TeamORM = relationship("TeamORM", foreign_keys="FixtureORM.away_team_name")

    @classmethod
    def from_football_fixture(cls, football_fixture: FootballFixture) -> FixtureORM:
        return cls(
            home_team_name=football_fixture.home_team_name,
            away_team_name=football_fixture.away_team_name,
            home_team_goals=football_fixture.home_team_goals,
            away_team_goals=football_fixture.away_team_goals,
            home_team_won=football_fixture.home_team_winner,
            away_team_won=football_fixture.away_team_winner,
            kick_off=football_fixture.kick_off,
            venue_city=football_fixture.venue_city,
            venue_name=football_fixture.venue_name,
            round=football_fixture.round,
        )
