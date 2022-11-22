from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from src.shared.football_api.responses import FixtureResponse
from src.shared.football_api.responses import TeamResponse


class FootballTeam(BaseModel):
    name: str

    @classmethod
    def from_response(cls, response: TeamResponse) -> FootballTeam:
        return cls(name=response["team"]["name"])


class FootballFixture(BaseModel):
    football_api_id: str
    home_team_name: str
    away_team_name: str
    home_team_goals: Optional[int]
    away_team_goals: Optional[int]
    home_team_winner: Optional[bool]
    away_team_winner: Optional[bool]
    kick_off: datetime
    venue_city: str
    venue_name: str
    round: str

    @classmethod
    def from_response(cls, response: FixtureResponse) -> FootballFixture:
        fixture = cls(
            football_api_id=response["fixture"]["id"],
            home_team_name=response["teams"]["home"]["name"],
            away_team_name=response["teams"]["away"]["name"],
            home_team_goals=response["goals"]["home"],
            away_team_goals=response["goals"]["away"],
            home_team_winner=response["teams"]["home"]["winner"],
            away_team_winner=response["teams"]["away"]["winner"],
            kick_off=datetime.fromisoformat(response["fixture"]["date"]),
            venue_city=response["fixture"]["venue"]["city"],
            venue_name=response["fixture"]["venue"]["name"],
            round=response["league"]["round"],
        )
        return fixture
