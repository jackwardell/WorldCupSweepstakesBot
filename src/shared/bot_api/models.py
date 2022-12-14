from __future__ import annotations

from typing import Optional

from src.shared.bot_api.db import FixtureORM
from src.shared.bot_api.db import ParticipantORM
from src.shared.bot_api.db import SweepstakeCategoryORM
from src.shared.bot_api.db import TeamORM
from src.shared.emoji import COUNTRIES_AND_FLAGS
from src.shared.schemas import FixtureEventSchema
from src.shared.schemas import FixtureSchema
from src.shared.schemas import ParticipantSchema
from src.shared.schemas import PlayerSchema
from src.shared.schemas import SweepstakeCategoryIDEnum
from src.shared.schemas import SweepstakeCategorySchema
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

    @property
    def name_and_emoji(self) -> str:
        return f"{self.name} {self.emoji}"

    @property
    def emoji_and_name(self) -> str:
        return f"{self.emoji} {self.name}"

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
            "???? Teams: {home_team_name} {home_team_emoji} "
            "play {away_team_name} {away_team_emoji}\n"
            "??????? Stadium: {venue_name} in {venue_city} ??????????????????\n"
            "???? Kick Off: {kick_off} today ??????\n"
            "???? Round: {round} ????\n"
            "?????? Rivals: {home_participant_tag} vs. {away_participant_tag} ????"
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
        # first_msg = "Well done"
        # if self.home_team_winner is None and self.away_team_winner is None:
        #     home_team_match_result = "drew with"
        #     home_team_insult_result = "and"
        #     winner_participant_tag = self.home_team.participant.telegram_tag
        #     loser_participant_tag = self.away_team.participant.telegram_tag
        # elif self.home_team_goals > self.away_team_goals and self.home_team_winner:
        #     home_team_match_result = "beat"
        #     home_team_insult_result = "and get rekt"
        #     winner_participant_tag = self.home_team.participant.telegram_tag
        #     loser_participant_tag = self.away_team.participant.telegram_tag
        # elif self.away_team_goals > self.home_team_goals and self.away_team_winner:
        #     home_team_match_result = "lost to"
        #     home_team_insult_result = "and get rekt"
        #     winner_participant_tag = self.away_team.participant.telegram_tag
        #     loser_participant_tag = self.home_team.participant.telegram_tag
        # else:
        #     home_team_match_result = "lost to" if self.away_team_winner else "beat"
        #     home_team_insult_result = "and get rekt"
        #     winner_participant_tag = self.away_team.participant.telegram_tag if
        #     self.away_team_winner else self.home_team.participant.telegram_tag
        #     loser_participant_tag = self.home_team.participant.telegram_tag if
        #     self.away_team_winner else self.away_team.participant.telegram_tag
        #
        # if self.home_team.participant.telegram_user_id == self.away_team.participant.telegram_user_id:
        #     home_team_insult_result = ""
        #     first_msg = "Well done/Get rekt"
        #     winner_participant_tag = self.away_team.participant.telegram_tag
        #     loser_participant_tag = self.home_team.participant.telegram_tag
        #
        # if self.home_goals_extratime is not None or self.away_goals_extratime is not None:
        #     extratime = f"{self.home_goals_extratime}-{self.away_goals_extratime} in ET"
        # else:
        #     extratime = ""
        # if self.home_goals_penalties is not None or self.away_goals_penalties is not None:
        #     penalties = f"{self.home_goals_penalties}-{self.away_goals_penalties} in Penalties"
        # else:
        #     penalties = ""
        # message = (
        #     "???? {home_team_name} {home_team_emoji} {home_team_match_result} {away_team_name} {away_team_emoji} "
        #     "{home_team_goals}-{away_team_goals} in FT {extratime} {penalties} ???\n"
        #     "???? {first_msg} {winner_participant_tag} {home_team_insult_result} {loser_participant_tag} ????"
        # ).format(
        #     home_team_name=self.home_team.name,
        #     home_team_emoji=self.home_team.emoji,
        #     home_team_match_result=home_team_match_result,
        #     away_team_name=self.away_team.name,
        #     away_team_emoji=self.away_team.emoji,
        #     home_team_goals=self.home_team_goals,
        #     away_team_goals=self.away_team_goals,
        #     extratime=extratime,
        #     penalties=penalties,
        #     winner_participant_tag=winner_participant_tag,
        #     loser_participant_tag=loser_participant_tag,
        #     first_msg=first_msg,
        #     home_team_insult_result=home_team_insult_result,
        # )
        # # return message

        msg = (
            f"???? {self.home_team.name_and_emoji} {self.home_to_away_comparison} {self.away_team.name_and_emoji} ???\n"
            f"???? {self.analysis} ???\n"
            f"???? Well done {self.winner_participant.telegram_tag} and get rekt {self.loser_participant.telegram_tag} ????"
        )
        return msg

    @property
    def winner_participant(self) -> Participant:
        return self.winner_team.participant

    @property
    def loser_participant(self) -> Participant:
        return self.loser_team.participant

    @property
    def winner_team(self) -> Team:
        if self.home_team_winner:
            return self.home_team
        else:
            return self.away_team

    @property
    def loser_team(self) -> Team:
        if self.away_team_winner:
            return self.home_team
        else:
            return self.away_team

    @property
    def full_time_analysis(self) -> str:
        if self.home_goals_extratime is None and self.away_goals_extratime is None:
            ft_home_goals = self.home_team_goals
            ft_away_goals = self.away_team_goals
        else:
            ft_home_goals = self.home_goals_fulltime
            ft_away_goals = self.away_goals_fulltime
        return (
            f"The score was {self.home_goals_halftime}-{self.away_goals_halftime} "
            f"by HT and {ft_home_goals}-{ft_away_goals} at FT"
        )

    @property
    def extra_time_analysis(self) -> str:
        if self.home_goals_extratime is None and self.away_goals_extratime is None:
            return ""
        return f"{self.home_goals_extratime}-{self.away_goals_extratime} in ET"

    @property
    def penalties_analysis(self) -> str:
        if self.home_goals_penalties is None and self.away_goals_penalties is None:
            return ""
        return f"and concluded in a penalty shootout: {self.home_goals_penalties}-{self.away_goals_penalties}"

    @property
    def analysis(self) -> str:
        if self.full_time_analysis and not self.extra_time_analysis and not self.penalties_analysis:
            return self.full_time_analysis
        if self.full_time_analysis and self.extra_time_analysis and not self.penalties_analysis:
            return self.full_time_analysis + " and " + self.extra_time_analysis
        if self.extra_time_analysis and self.extra_time_analysis and self.penalties_analysis:
            return self.full_time_analysis + ", " + self.extra_time_analysis + " " + self.penalties_analysis

    @property
    def home_to_away_comparison(self) -> str:
        if self.home_team_winner is None and self.away_team_winner is None:
            return "drew with"
        if self.home_team_goals - self.away_team_goals >= 4:
            return "annihilated"
        if self.home_team_goals - self.away_team_goals == 3:
            return "destroyed"
        if self.home_team_goals - self.away_team_goals == 2:
            return "smashed"
        if self.home_team_goals - self.away_team_goals == 1:
            return "beat"
        if self.away_team_goals - self.home_team_goals >= 4:
            return "were annihilated by"
        if self.away_team_goals - self.home_team_goals == 3:
            return "were destroyed by"
        if self.away_team_goals - self.home_team_goals == 2:
            return "were smashed by"
        if self.away_team_goals - self.home_team_goals == 1:
            return "lost to"
        else:
            return "lost to" if self.away_team_winner else "beat"

    @property
    def matching_participants(self) -> bool:
        return self.home_team.participant.telegram_user_id == self.away_team.participant.telegram_user_id


class Player(PlayerSchema):
    ...


class FixtureEvent(FixtureEventSchema):
    ...


class SweepstakeCategory(SweepstakeCategorySchema):
    ...

    @classmethod
    def from_orm(cls, sweepstake_category: SweepstakeCategoryORM) -> SweepstakeCategory:
        return SweepstakeCategory(
            id=SweepstakeCategoryIDEnum(sweepstake_category.id),
            name=sweepstake_category.name,
            reward_amount=sweepstake_category.reward_amount,
        )
