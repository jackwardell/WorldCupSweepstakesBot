from __future__ import annotations

from datetime import date
from datetime import datetime
from typing import List
from typing import Optional

from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from src.shared.football_api.models import FootballFixture
from src.shared.football_api.models import FootballTeam
from src.shared.telegram_api.models import TelegramParticipant

Base = declarative_base()


class ParticipantORM(Base):
    __tablename__ = "participant"

    telegram_user_id: int = Column(BigInteger, primary_key=True, nullable=False)
    first_name: str = Column(String, nullable=False)

    draw_mappings: List[DrawMappingORM] = relationship(
        "DrawMappingORM",
        back_populates="participant",
        uselist=True,
    )

    @classmethod
    def from_telegram_user(cls, telegram_user: TelegramParticipant) -> ParticipantORM:
        return cls(first_name=telegram_user.first_name, telegram_user_id=telegram_user.telegram_user_id)


class TeamORM(Base):
    __tablename__ = "team"

    football_api_id: int = Column(Integer, primary_key=True, nullable=False)
    name: str = Column(String, nullable=False)

    draw_mapping: DrawMappingORM = relationship(
        "DrawMappingORM",
        back_populates="team",
        uselist=False,
    )

    @classmethod
    def from_football_team(cls, football_team: FootballTeam) -> TeamORM:
        return cls(football_api_id=football_team.football_api_id, name=football_team.name)


class DrawMappingORM(Base):
    __tablename__ = "draw_mapping"

    team_football_api_id: int = Column(Integer, ForeignKey("team.football_api_id"), primary_key=True, nullable=False)
    participant_telegram_user_id: int = Column(
        BigInteger, ForeignKey("participant.telegram_user_id"), primary_key=True, nullable=False
    )

    team: TeamORM = relationship(
        "TeamORM",
        back_populates="draw_mapping",
        uselist=False,
    )
    participant: ParticipantORM = relationship(
        "ParticipantORM",
        back_populates="draw_mappings",
        uselist=False,
    )

    __table_args__ = (
        UniqueConstraint("team_football_api_id", "participant_telegram_user_id", name="one_team_per_participant"),
    )

    @classmethod
    def from_team_football_api_id_and_participant_telegram_user_id(
        cls,
        team_football_api_id: int,
        participant_telegram_user_id: int,
    ) -> TeamORM:
        return cls(
            team_football_api_id=team_football_api_id,
            participant_telegram_user_id=participant_telegram_user_id,
        )


class FixtureORM(Base):
    __tablename__ = "fixture"

    football_api_id: str = Column(Integer, primary_key=True, nullable=False)
    home_team_football_api_id: int = Column(Integer, ForeignKey("team.football_api_id"), nullable=False)
    away_team_football_api_id: int = Column(Integer, ForeignKey("team.football_api_id"), nullable=False)
    home_team_goals: Optional[int] = Column(Integer, nullable=True)
    away_team_goals: Optional[int] = Column(Integer, nullable=True)
    home_team_won: Optional[bool] = Column(Boolean, nullable=True)
    away_team_won: Optional[bool] = Column(Boolean, nullable=True)
    venue_name: str = Column(String, nullable=False)
    venue_city: str = Column(String, nullable=False)
    kick_off: datetime = Column(DateTime, nullable=False)
    round: str = Column(String, nullable=False)
    home_goals_halftime: Optional[int] = Column(Integer, nullable=True)
    away_goals_halftime: Optional[int] = Column(Integer, nullable=True)
    home_goals_fulltime: Optional[int] = Column(Integer, nullable=True)
    away_goals_fulltime: Optional[int] = Column(Integer, nullable=True)
    away_goals_extratime: Optional[int] = Column(Integer, nullable=True)
    home_goals_extratime: Optional[int] = Column(Integer, nullable=True)
    home_goals_penalties: Optional[int] = Column(Integer, nullable=True)
    away_goals_penalties: Optional[int] = Column(Integer, nullable=True)

    home_team: TeamORM = relationship("TeamORM", foreign_keys="FixtureORM.home_team_football_api_id")
    away_team: TeamORM = relationship("TeamORM", foreign_keys="FixtureORM.away_team_football_api_id")

    @classmethod
    def from_football_fixture(cls, football_fixture: FootballFixture) -> FixtureORM:
        return cls(
            football_api_id=football_fixture.football_api_id,
            home_team_football_api_id=football_fixture.home_team_football_api_id,
            away_team_football_api_id=football_fixture.away_team_football_api_id,
            home_team_goals=football_fixture.home_team_goals,
            away_team_goals=football_fixture.away_team_goals,
            home_team_won=football_fixture.home_team_winner,
            away_team_won=football_fixture.away_team_winner,
            kick_off=football_fixture.kick_off,
            venue_city=football_fixture.venue_city,
            venue_name=football_fixture.venue_name,
            round=football_fixture.round,
            home_goals_halftime=football_fixture.home_goals_halftime,
            away_goals_halftime=football_fixture.away_goals_halftime,
            home_goals_fulltime=football_fixture.home_goals_fulltime,
            away_goals_fulltime=football_fixture.away_goals_fulltime,
            home_goals_extratime=football_fixture.home_goals_extratime,
            away_goals_extratime=football_fixture.away_goals_extratime,
            home_goals_penalties=football_fixture.home_goals_penalties,
            away_goals_penalties=football_fixture.away_goals_penalties,
        )


class FixtureEventORM(Base):
    id: int = Column(Integer, primary_key=True, nullable=False)
    time_elapsed_min: int = Column(Integer, nullable=False)
    time_elapsed_extra_min: Optional[int] = Column(Integer, nullable=True)
    team_football_api_id: int = Column(Integer, ForeignKey("team.football_api_id"), nullable=False)
    player_football_api_id: int = Column(Integer, ForeignKey("player.football_api_id"), nullable=False)
    type: str = Column(String, nullable=False)
    detail: str = Column(String, nullable=False)


class PlayerORM(Base):
    football_api_id: int = Column(Integer, primary_key=True, nullable=False)
    first_name: str = Column(String, nullable=False)
    last_name: str = Column(String, nullable=False)
    date_of_birth: date = Column(Date, nullable=False)
    team_football_api_id: int = Column(Integer, ForeignKey("team.football_api_id"), nullable=False)
    yellow_cards: Optional[int] = Column(Integer, nullable=True)
    yellow_then_red_cards: Optional[int] = Column(Integer, nullable=True)
    red_cards: Optional[int] = Column(Integer, nullable=True)
    goals: Optional[int] = Column(Integer, nullable=True)


class SweepstakeCategoryORM(Base):
    id: int = Column(Integer, primary_key=True, nullable=False)
    name: str = Column(String, nullable=False)
    reward_amount: int = Column(Integer, nullable=False)
    winning_team_football_api_id: int = Column(Integer, ForeignKey("team.football_api_id"), nullable=True)
    winning_player_football_api_id: int = Column(Integer, ForeignKey("player.football_api_id"), nullable=True)
