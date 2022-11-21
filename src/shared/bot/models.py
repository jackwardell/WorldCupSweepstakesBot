from __future__ import annotations

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from src.shared.emoji import COUNTRIES_AND_FLAGS
from src.shared.football_api.models import FootballFixture

from src.shared.db.models import ParticipantORM, TeamORM, TeamAndParticipantORM, FixtureORM


class Participant(BaseModel):
    name: str
    telegram_id: int

    @property
    def tagged_telegram_participant(self) -> str:
        return f"[{self.name}](tg://user?id={self.telegram_id})"

    @classmethod
    def from_orm(cls, participant: ParticipantORM) -> Participant:
        return cls(name=participant.name, telegram_id=participant.telegram_id)


class Team(BaseModel):
    name: str

    @property
    def emoji(self) -> str:
        return COUNTRIES_AND_FLAGS[self.name]

    @classmethod
    def from_orm(cls, team: TeamORM) -> Team:
        return cls(name=team.name)


class Fixture(BaseModel):
    home_team: Team
    away_team: Team
    home_participant: Participant
    away_participant: Participant
    home_team_goals: Optional[int]
    away_team_goals: Optional[int]
    home_team_won: Optional[bool]
    away_team_won: Optional[bool]
    kick_off: datetime
    venue_name: str
    venue_city: str
    round: str

    # @classmethod
    # def from_football_fixture(cls, football_fixture: FootballFixture) -> Fixture:
    #     fixture = cls(
    #         home_team_result=TeamResult(
    #             team=Team(name=football_fixture.home_team_name),
    #             goals=football_fixture.home_goals,
    #             winner=football_fixture.home_winner,
    #         ),
    #         away_team_result=TeamResult(
    #             team=Team(name=football_fixture.away_team_name),
    #             goals=football_fixture.away_goals,
    #             winner=football_fixture.away_winner,
    #         ),
    #         kick_off=football_fixture.kick_off,
    #         venue=Venue(
    #             name=football_fixture.venue_name,
    #             city=football_fixture.venue_city,
    #         ),
    #         round=football_fixture.round,
    #     )
    #     return fixture

    @classmethod
    def from_orm(cls, fixture: FixtureORM) -> Fixture:
        return cls(
            home_team=Team.from_orm(fixture.home_team),
            away_team=Team.from_orm(fixture.away_team),
            # home_participant=home_participant,
            # away_participant=away_participant,
            home_participant=Participant.from_orm(fixture.home_team.participant.participant),
            away_participant=Participant.from_orm(fixture.away_team.participant.participant),
            home_team_goals=fixture.home_team_goals,
            away_team_goals=fixture.away_team_goals,
            home_team_won=fixture.home_team_won,
            away_team_won=fixture.away_team_won,
            kick_off=fixture.kick_off,
            venue_name=fixture.venue_name,
            venue_city=fixture.venue_city,
            round=fixture.round,
        )

    @property
    def morning_message(self) -> str:
        message = (
            "🤝 Teams: {home_team_name} {home_team_emoji} play {away_team_name} {away_team_emoji}\n"
            "🏟️ Stadium: {venue_name} in {venue_city} 🧑‍🤝‍🧑\n"
            "🦵 Kick Off: {kick_off} today ⏱️\n"
            "🔢 Round: {round} 💫\n"
            "⚔️ Rivals: {home_participant_tag} vs. {away_participant_tag} 😈\n"
        ).format(
            home_team_name=self.home_team.name,
            home_team_emoji=self.home_team.emoji,
            away_team_name=self.away_team.name,
            away_team_emoji=self.away_team.emoji,
            venue_name=self.venue_name,
            venue_city=self.venue_city,
            kick_off=self.kick_off,
            round=self.round,
            home_participant_tag=self.home_participant.tagged_telegram_participant,
            away_participant_tag=self.away_participant.tagged_telegram_participant
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
