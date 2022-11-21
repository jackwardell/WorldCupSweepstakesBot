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

    # @property
    # def morning_message(self) -> str:
    #     message = (
    #         "🤝 Teams: {home_team_name} {home_team_emoji} play {away_team_name} {away_team_emoji} \n"
    #         "🏟️Stadium: {venue_name} in {venue_city} 🧑‍🤝‍🧑\n"
    #         "🦵 Kick Off: {kick_off} today ⏱️\n"
    #         "🔢 Round: {round} 💫\n"
    #         "⚔️ Rivals: [{home_rival_name}](tg://user?id={home_rival_telegram_id}) "
    #         "vs. [{away_rival_name}](tg://user?id={away_rival_telegram_id}) 😈"
    #     ).format(
    #         home_team_name=self.home_team.name,
    #         home_team_emoji=self.home_team.emoji,
    #         away_team_name=self.away_team.name,
    #         away_team_emoji=self.away_team.emoji,
    #         venue_name=self.venue_name,
    #         venue_city=self.venue_city,
    #         kick_off=self.kick_off.time(),
    #         round=self.round,
    #         home_rival_name=self.home_team.participant.display_name,
    #         away_rival_name=self.away_team.participant.display_name,
    #         home_rival_telegram_id=self.home_team.participant.telegram_id,
    #         away_rival_telegram_id=self.away_team.participant.telegram_id,
    #     )
    #     return message
    #
    # @property
    # def home_and_away_rivals_equal(self) -> bool:
    #     return self.home_team.participant == self.away_team.participant
