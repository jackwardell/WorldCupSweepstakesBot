from __future__ import annotations

from typing import Optional

from src.shared.bot_api.db import FixtureORM
from src.shared.bot_api.db import ParticipantORM
from src.shared.bot_api.db import TeamORM
from src.shared.emoji import COUNTRIES_AND_FLAGS
from src.shared.schemas import FixtureEventSchema
from src.shared.schemas import FixtureSchema
from src.shared.schemas import ParticipantSchema
from src.shared.schemas import PlayerSchema
from src.shared.schemas import TeamSchema


class Participant(ParticipantSchema):
    @property
    def telegram_tag(self) -> str:
        return f"[{self.first_name}](tg://user?id={self.telegram_user_id})"

    @classmethod
    def from_orm(cls, participant: ParticipantORM) -> Participant:
        return cls(first_name=participant.first_name, telegram_user_id=participant.telegram_user_id)


class Team(TeamSchema):
    participant: Optional[Participant]

    @property
    def emoji(self) -> str:
        return COUNTRIES_AND_FLAGS[self.name]

    @classmethod
    def from_orm(cls, team: TeamORM) -> Team:
        return cls(
            football_api_id=team.football_api_id,
            name=team.name,
            participant=Participant.from_orm(team.draw_mapping.participant) if team.draw_mapping else None,
        )


class Fixture(FixtureSchema):
    home_team: Team
    away_team: Team

    @classmethod
    def from_orm(cls, fixture: FixtureORM) -> Fixture:
        return cls(
            football_api_id=fixture.football_api_id,
            home_team=Team.from_orm(fixture.home_team),
            away_team=Team.from_orm(fixture.away_team),
            home_team_goals=fixture.home_team_goals,
            away_team_goals=fixture.away_team_goals,
            home_team_winner=fixture.home_team_won,
            away_team_winner=fixture.away_team_won,
            kick_off=fixture.kick_off,
            venue_name=fixture.venue_name,
            venue_city=fixture.venue_city,
            round=fixture.round,
            home_goals_halftime=fixture.home_goals_halftime,
            away_goals_halftime=fixture.away_goals_halftime,
            home_goals_fulltime=fixture.home_goals_fulltime,
            away_goals_fulltime=fixture.away_goals_fulltime,
            home_goals_extratime=fixture.away_goals_extratime,
            away_goals_extratime=fixture.home_goals_extratime,
            home_goals_penalties=fixture.home_goals_penalties,
            away_goals_penalties=fixture.away_goals_penalties,
        )

    @property
    def morning_message(self) -> str:
        message = (
            "🤝 Teams: {home_team_name} {home_team_emoji} "
            "play {away_team_name} {away_team_emoji}\n"
            "🏟️ Stadium: {venue_name} in {venue_city} 🧑‍🤝‍🧑\n"
            "🦵 Kick Off: {kick_off} today ⏱️\n"
            "🔢 Round: {round} 💫\n"
            "⚔️ Rivals: {home_participant_tag} vs. {away_participant_tag} 😈"
        ).format(
            home_team_name=self.home_team.name,
            home_team_emoji=self.home_team.emoji,
            away_team_name=self.away_team.name,
            away_team_emoji=self.away_team.emoji,
            venue_name=self.venue_name,
            venue_city=self.venue_city,
            kick_off=self.kick_off.time(),
            round=self.round,
            home_participant_tag=self.home_team.participant.telegram_tag,
            away_participant_tag=self.away_team.participant.telegram_tag,
        )
        return message

    @property
    def evening_message(self) -> str:
        first_msg = "Well done"
        if self.home_team_won is None and self.away_team_won is None:
            home_team_match_result = "drew with"
            home_team_insult_result = "and"
            winner_participant_tag = self.home_participant.telegram_tag
            loser_participant_tag = self.away_participant.telegram_tag
        elif self.home_team_goals > self.away_team_goals and self.home_team_won:
            home_team_match_result = "beat"
            home_team_insult_result = "and get rekt"
            winner_participant_tag = self.home_participant.telegram_tag
            loser_participant_tag = self.away_participant.telegram_tag
        elif self.away_team_goals > self.home_team_goals and self.away_team_won:
            home_team_match_result = "lost to"
            home_team_insult_result = "and get rekt"
            winner_participant_tag = self.away_participant.telegram_tag
            loser_participant_tag = self.home_participant.telegram_tag
        else:
            raise ValueError("hmmm?")

        if self.home_participant.name == self.away_participant.name:
            home_team_insult_result = ""
            first_msg = "Well done/Get rekt"
            winner_participant_tag = self.away_participant.telegram_tag
            loser_participant_tag = self.home_participant.telegram_tag
        message = (
            "🏆 {home_team_name} {home_team_emoji} {home_team_match_result} {away_team_name} {away_team_emoji} "
            "{home_team_goals}-{away_team_goals} ⚽\n"
            "🎉 {first_msg} {winner_participant_tag} {home_team_insult_result} {loser_participant_tag} 💀"
        ).format(
            home_team_name=self.home_team.name,
            home_team_emoji=self.home_team.emoji,
            home_team_match_result=home_team_match_result,
            away_team_name=self.away_team.name,
            away_team_emoji=self.away_team.emoji,
            home_team_goals=self.home_team_goals,
            away_team_goals=self.away_team_goals,
            winner_participant_tag=winner_participant_tag,
            loser_participant_tag=loser_participant_tag,
            first_msg=first_msg,
            home_team_insult_result=home_team_insult_result,
        )
        return message

    @property
    def matching_participants(self) -> bool:
        return self.home_participant.name == self.away_participant.name


class Player(PlayerSchema):
    ...


class FixtureEvent(FixtureEventSchema):
    ...
