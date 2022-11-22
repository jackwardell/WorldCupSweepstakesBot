from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from src.shared.bot_api.db import FixtureORM
from src.shared.bot_api.db import ParticipantORM
from src.shared.bot_api.db import TeamAndParticipantORM
from src.shared.bot_api.db import TeamORM
from src.shared.emoji import COUNTRIES_AND_FLAGS


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


class TeamAndParticipant(BaseModel):
    team: Team
    participant: Participant

    @classmethod
    def from_orm(cls, team_and_participant: TeamAndParticipantORM) -> TeamAndParticipant:
        return cls(team=team_and_participant.team, participant=team_and_participant.participant)


class Fixture(BaseModel):
    id: int
    football_api_id: str
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

    @classmethod
    def from_orm(cls, fixture: FixtureORM) -> Fixture:
        return cls(
            id=fixture.id,
            football_api_id=fixture.football_api_id,
            home_team=Team.from_orm(fixture.home_team),
            away_team=Team.from_orm(fixture.away_team),
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
            "🤝 Teams: {home_team_name} {home_team_emoji} "
            "play {away_team_name} {away_team_emoji}\n"
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
            kick_off=self.kick_off.time(),
            round=self.round,
            home_participant_tag=self.home_participant.tagged_telegram_participant,
            away_participant_tag=self.away_participant.tagged_telegram_participant,
        )
        return message

    @property
    def evening_message(self) -> str:
        if self.home_team_won is None and self.away_team_won is None:
            home_team_won_or_lost = "drew with"
            other_msg = "and"
        elif self.home_team_goals > self.away_team_goals and self.home_team_won:
            home_team_won_or_lost = "beat"
            other_msg = "and get rekt"
        elif self.away_team_goals > self.home_team_goals and self.away_team_won:
            home_team_won_or_lost = "lost to"
            other_msg = "and get rekt"
        else:
            raise ValueError("hmmm?")
        message = (
            "🏆 {home_team_name} {home_team_emoji} {home_team_won_or_lost} {away_team_name} {away_team_emoji} "
            "{home_team_goals}-{away_team_goals} ⚽\n"
            "🎉 Well done {home_participant_tag} {other_msg} {away_participant_tag} 💀"
        ).format(
            home_team_name=self.home_team.name,
            home_team_emoji=self.home_team.emoji,
            home_team_won_or_lost=home_team_won_or_lost,
            away_team_name=self.away_team.name,
            away_team_emoji=self.away_team.emoji,
            home_team_goals=self.home_team_goals,
            away_team_goals=self.away_team_goals,
            home_participant_tag=self.home_participant.tagged_telegram_participant
            if self.home_participant.name != "Lucy"
            else self.away_participant.tagged_telegram_participant,
            away_participant_tag=self.away_participant.tagged_telegram_participant
            if self.home_participant.name != "Lucy"
            else self.home_participant.tagged_telegram_participant,
            other_msg=other_msg,
        )
        return message


# class FixtureCollection(BaseModel):
#     fixtures: List[Fixture]
#
#     @classmethod
#     def from_fixtures(cls, fixtures: List[FixtureORM]) -> FixtureCollection:
#         return cls(fixtures=[Fixture.from_orm(f) for f in fixtures])
#
#     @property
#     def fixture_message(self) -> str:
#         if len(self.fixtures) == 0:
#             fixture_message = "No fixtures today, just chill the fuck out 🍻"
#         elif len(self.fixtures) == 1:
#             fixture_message = "Today there is one match. Here's the fixture 👇"
#         else:
#             fixture_message = f"Today there {len(self.fixtures)} matches. Here are the fixtures 👇"
#         return fixture_message
