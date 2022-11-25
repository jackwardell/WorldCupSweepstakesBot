from __future__ import annotations

from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from src.shared.football_api.responses import FixturesFixturesResponse
from src.shared.football_api.responses import PlayerPlayerResponse
from src.shared.football_api.responses import TeamTeamInformationResponse


class FootballTeam(BaseModel):
    football_api_id: int
    name: str

    @classmethod
    def from_response(cls, response: TeamTeamInformationResponse) -> FootballTeam:
        team = cls(
            id=response["team"]["id"],
            name=response["team"]["name"],
        )
        return team


class FootballFixture(BaseModel):
    football_api_id: int
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
    home_goals_halftime: Optional[int]
    away_goals_halftime: Optional[int]
    home_goals_fulltime: Optional[int]
    away_goals_fulltime: Optional[int]
    away_goals_extratime: Optional[int]
    home_goals_extratime: Optional[int]
    home_goals_penalties: Optional[int]
    away_goals_penalties: Optional[int]

    @classmethod
    def from_response(cls, response: FixturesFixturesResponse) -> FootballFixture:
        fixture = cls(
            id=response["fixture"]["id"],
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
            home_goals_halftime=response["score"]["halftime"]["home"],
            away_goals_halftime=response["score"]["halftime"]["away"],
            home_goals_fulltime=response["score"]["fulltime"]["home"],
            away_goals_fulltime=response["score"]["fulltime"]["away"],
            away_goals_extratime=response["score"]["extratime"]["home"],
            home_goals_extratime=response["score"]["extratime"]["away"],
            home_goals_penalties=response["score"]["penalty"]["home"],
            away_goals_penalties=response["score"]["penalty"]["away"],
        )
        return fixture


class FootballPlayer(BaseModel):
    football_api_id: int
    first_name: str
    last_name: str
    date_of_birth: date
    team_name: str
    team_football_api_id: int
    yellow_cards: Optional[int]
    yellow_then_red_cards: Optional[int]
    red_cards: Optional[int]
    goals: Optional[int]

    @classmethod
    def from_response(cls, response: PlayerPlayerResponse) -> FootballPlayer:
        assert len(response["statistics"]) == 1
        player = cls(
            football_api_id=response["player"]["id"],
            first_name=response["player"]["firstname"],
            last_name=response["player"]["lastname"],
            date_of_birth=date.fromisoformat(response["player"]["birth"]["date"]),
            team_name=response["statistics"][0]["team"]["name"],
            team_football_api_id=response["statistics"][0]["team"]["id"],
            yellow_cards=response["statistics"][0]["cards"]["yellow"],
            yellow_then_red_cards=response["statistics"][0]["cards"]["yellowred"],
            red_cards=response["statistics"][0]["cards"]["red"],
            goals=response["statistics"][0]["goals"]["total"],
        )
        return player
