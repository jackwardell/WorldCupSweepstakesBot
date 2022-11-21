from __future__ import annotations
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, BigInteger
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from src.shared.telegram_api.models import TelegramUser
from src.shared.football_api.models import FootballTeam
from datetime import datetime
from src.shared.football_api.models import FootballFixture
Base = declarative_base()


class ParticipantORM(Base):
    __tablename__ = "participant"

    name: str = Column(String, primary_key=True, nullable=False)
    telegram_id: int = Column(BigInteger, nullable=False)

    team: TeamORM = relationship("TeamParticipantAssociationORM", back_populates="participant")

    @classmethod
    def from_telegram_user(cls, telegram_user: TelegramUser) -> ParticipantORM:
        return cls(name=telegram_user.first_name, telegram_id=telegram_user.id)


class TeamORM(Base):
    __tablename__ = "team"

    name: str = Column(String, primary_key=True, nullable=False)

    participant: ParticipantORM = relationship("TeamParticipantAssociationORM", back_populates="team")

    @classmethod
    def from_football_team(cls, football_team: FootballTeam) -> TeamORM:
        return cls(name=football_team.name)


class TeamParticipantAssociationORM(Base):
    __tablename__ = "team_participant_association"

    id: int = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    team_name: str = Column(String, ForeignKey("team.name"), nullable=False)
    participant_name: str = Column(String, ForeignKey("participant.name"), nullable=False)

    team: TeamORM = relationship("TeamORM", back_populates="participant")
    participant: ParticipantORM = relationship("ParticipantORM", back_populates="team")


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
        return cls(home_team_name=football_fixture.home_team_name, away_team_name=football_fixture.away_team_name, )