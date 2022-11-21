from __future__ import annotations

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from src.shared.emoji import COUNTRIES_AND_FLAGS
from src.shared.football_api.models import FootballFixture

from src.shared.db.models import ParticipantORM, TeamORM, TeamParticipantAssociationORM


class Participant(BaseModel):
    id: int
    name: str
    telegram_id: int

    @property
    def tagged_telegram_participant(self) -> str:
        return f"[{self.name}](tg://user?id={self.telegram_id})"

    @classmethod
    def from_orm(cls, participant: ParticipantORM) -> Participant:
        return cls(id=participant.id, name=participant.name, telegram_id=participant.telegram_id)


class Team(BaseModel):
    id: int
    name: str

    @property
    def emoji(self) -> str:
        return COUNTRIES_AND_FLAGS[self.name]

    @classmethod
    def from_orm(cls, team: TeamORM) -> Team:
        return cls(id=team.id, name=team.name)


class TeamResult(BaseModel):
    team: Team
    goals: Optional[int]
    winner: bool
    participant: Participant

    @property
    def won_or_lost(self) -> str:
        return "won against" if self.winner else "lost to"


class Venue(BaseModel):
    city: str
    name: str


class Fixture(BaseModel):
    home_team_result: TeamResult
    away_team_result: TeamResult
    kick_off: datetime
    venue: Venue
    round: str

    @classmethod
    def from_football_fixture(cls, football_fixture: FootballFixture) -> Fixture:
        fixture = cls(
            home_team_result=TeamResult(
                team=Team(name=football_fixture.home_team_name),
                goals=football_fixture.home_goals,
                winner=football_fixture.home_winner,
            ),
            away_team_result=TeamResult(
                team=Team(name=football_fixture.away_team_name),
                goals=football_fixture.away_goals,
                winner=football_fixture.away_winner,
            ),
            kick_off=football_fixture.kick_off,
            venue=Venue(
                name=football_fixture.venue_name,
                city=football_fixture.venue_city,
            ),
            round=football_fixture.round,
        )
        return fixture

    @property
    def morning_message(self) -> str:
        message = (
            "🏆 {home_team_name} {home_team_emoji} {home_team_won_or_lost} {away_team_name} {away_team_emoji} "
            "{home_team_goals}-{away_team_goals} 😞\n"
            "🎉 Well done [{home_team_rival_name}](tg://user?id={home_team_rival_telegram_id}) and get rekt "
            "[{away_team_name}](tg://user?id={home_team_rival_telegram_id}) 💀"
        )
        return message

    @property
    def evening_message(self) -> str:
        message = (
            "🏆 {home_team_name} {home_team_emoji} {home_team_won_or_lost} {away_team_name} {away_team_emoji} "
            "{home_team_goals}-{away_team_goals} 😞\n"
            "🎉 Well done [{home_team_rival_name}](tg://user?id={home_team_rival_telegram_id}) and get rekt "
            "[{away_team_name}](tg://user?id={home_team_rival_telegram_id}) 💀"
        )
        return message


class FixtureCollections(BaseModel):
    fixtures: List[Fixture]

    @classmethod
    def from_football_fixtures(cls, football_fixtures: List[FootballFixture]) -> FixtureCollections:
        return cls(fixtures=[Fixture.from_football_fixture(f) for f in football_fixtures])

    @property
    def morning_intro_message(self) -> str:
        if len(self.fixtures) == 1:
            return f"Today there is 1 match. Here is the fixture 👇"
        else:
            return f"Today there are {len(self.fixtures)} matches. Here are the fixtures 👇"
