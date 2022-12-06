from __future__ import annotations

from collections import defaultdict
from datetime import date
from datetime import datetime
from functools import lru_cache
from typing import List
from typing import Optional
from typing import Tuple
from typing import TypedDict

import attr
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import or_
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from src.shared.bot_api.db import DrawMappingORM
from src.shared.bot_api.db import FixtureEventORM
from src.shared.bot_api.db import FixtureORM
from src.shared.bot_api.db import ParticipantORM
from src.shared.bot_api.db import PlayerORM
from src.shared.bot_api.db import SweepstakeCategoryORM
from src.shared.bot_api.db import TeamORM
from src.shared.bot_api.models import Fixture
from src.shared.bot_api.models import Participant
from src.shared.bot_api.models import Player
from src.shared.bot_api.models import SweepstakeCategory
from src.shared.bot_api.models import Team
from src.shared.config import get_config
from src.shared.football_api.models import FootballFixture
from src.shared.football_api.models import FootballFixtureEvent
from src.shared.football_api.models import FootballPlayer
from src.shared.football_api.models import FootballTeam
from src.shared.open_weather_map_api.api import get_open_weather_map_api
from src.shared.open_weather_map_api.api import OpenWeatherMapApi
from src.shared.schemas import FixtureEventTypeEnum
from src.shared.schemas import SweepstakeCategoryIDEnum
from src.shared.telegram_api.api import get_telegram_api
from src.shared.telegram_api.api import TelegramApi
from src.shared.telegram_api.models import TelegramParticipant


class BotApiError(Exception):
    pass


def zero_if_none(field: Optional[int]) -> int:
    return field if field else 0


class WorstTeamData(TypedDict):
    losses: int
    goals_scored: int
    goals_conceded: int


class FilthiestTeamData(TypedDict):
    yellow: int
    yellow_then_red: int
    red: int


class EarliestAndLatestGoalTeamData(TypedDict):
    minutes_elapsed: int
    player_full_name: str
    against_team_name: str
    date: date


class YoungestAndOldestGoalScorerData(TypedDict):
    player_full_name: str
    age: str


@lru_cache
def get_engine() -> Engine:
    return create_engine(get_config().POSTGRES_DSN)


@lru_cache
def get_bot_api() -> BotApi:
    return BotApi()


@attr.s
class BotApi:
    session: Session = attr.ib(factory=lambda: Session(get_engine()))
    telegram_api: TelegramApi = attr.ib(factory=get_telegram_api)
    open_weather_map_api: OpenWeatherMapApi = attr.ib(factory=get_open_weather_map_api)

    def get_number_of_fixtures_morning_message(self) -> str:
        fixtures = self.get_fixtures()
        if len(fixtures) == 0:
            return "No fixtures today, just chill the fuck out 🍻"
        elif len(fixtures) == 1:
            return "Today there is one match. Here's the fixture 👇"
        else:
            return f"Today there {len(fixtures)} matches. Here are the fixtures 👇"

    def get_participants(self) -> List[Participant]:
        with self.session as session:
            return [Participant.from_orm(p) for p in session.query(ParticipantORM).all()]

    def save_participant(self, telegram_user: TelegramParticipant) -> Participant:
        logger.info(f"saving participant: {telegram_user.telegram_user_id}")
        with self.session as session:
            participant = ParticipantORM.from_telegram_user(telegram_user)
            session.add(participant)
            try:
                session.commit()
                return Participant.from_orm(participant)
            except IntegrityError as e:
                session.rollback()
                raise BotApiError(e) from e

    def get_teams(self) -> List[Team]:
        with self.session as session:
            return [Team.from_orm(t) for t in session.query(TeamORM).all()]

    def get_team(self, football_api_id: int) -> Team:
        with self.session as session:
            return Team.from_orm(session.query(TeamORM).filter(TeamORM.football_api_id == football_api_id).one())

    def save_team(self, football_team: FootballTeam) -> Team:
        logger.info(f"saving team: {football_team.football_api_id} {football_team.name}")
        with self.session as session:
            team = TeamORM.from_football_team(football_team)
            session.add(team)
            try:
                session.commit()
                return Team.from_orm(team)
            except IntegrityError as e:
                session.rollback()
                raise BotApiError(e) from e

    def save_team_drawn_by_participant(self, team_football_api_id: int, participant_telegram_user_id: int) -> None:
        logger.info(f"saving draw_mapping:  {team_football_api_id} drawn by {participant_telegram_user_id}")
        with self.session as session:
            team_drawn_by_participant = DrawMappingORM.from_team_football_api_id_and_participant_telegram_user_id(
                team_football_api_id=team_football_api_id,
                participant_telegram_user_id=participant_telegram_user_id,
            )
            session.add(team_drawn_by_participant)
            try:
                session.commit()
                return
            except IntegrityError as e:
                session.rollback()
                raise BotApiError(e) from e

    def get_fixtures(self, today_only: bool = True) -> List[Fixture]:
        with self.session as session:
            if today_only:
                query = (
                    session.query(FixtureORM)
                    .filter(func.extract("month", FixtureORM.kick_off) == datetime.today().month)
                    .filter(func.extract("year", FixtureORM.kick_off) == datetime.today().year)
                    .filter(func.extract("day", FixtureORM.kick_off) == datetime.today().day)
                    .order_by(FixtureORM.kick_off)
                    .all()
                )
            else:
                query = session.query(FixtureORM).all()
            return [Fixture.from_orm(f) for f in query]

    def save_or_update_fixture(self, football_fixture: FootballFixture) -> Fixture:
        logger.info(f"saving or updating fixture: {football_fixture.football_api_id}")
        with self.session as session:
            fixture = session.query(FixtureORM).filter_by(football_api_id=football_fixture.football_api_id).first()
            if fixture:
                fixture.home_team_goals = football_fixture.home_team_goals
                fixture.away_team_goals = football_fixture.away_team_goals
                fixture.home_team_won = football_fixture.home_team_winner
                fixture.away_team_won = football_fixture.away_team_winner
                fixture.home_goals_halftime = football_fixture.home_goals_halftime
                fixture.away_goals_halftime = football_fixture.away_goals_halftime
                fixture.home_goals_fulltime = football_fixture.home_goals_fulltime
                fixture.away_goals_fulltime = football_fixture.away_goals_fulltime
                fixture.home_goals_extratime = football_fixture.home_goals_extratime
                fixture.away_goals_extratime = football_fixture.away_goals_extratime
                fixture.home_goals_penalties = football_fixture.home_goals_penalties
                fixture.away_goals_penalties = football_fixture.away_goals_penalties
            else:
                fixture = FixtureORM.from_football_fixture(football_fixture)
            session.add(fixture)
            session.commit()
            return Fixture.from_orm(fixture)

    def save_sweepstake_category(
        self,
        sweepstake_category_enum: SweepstakeCategoryIDEnum,
        sweepstake_category_name: str,
        sweepstake_category_reward_amount: int,
    ) -> None:
        logger.info(f"saving sweepstake_category: {sweepstake_category_name} {sweepstake_category_name}")
        with self.session as session:
            try:
                session.add(
                    SweepstakeCategoryORM(
                        id=sweepstake_category_enum.value,
                        name=sweepstake_category_name,
                        reward_amount=sweepstake_category_reward_amount,
                    )
                )
                session.commit()
            except IntegrityError:
                session.rollback()

    def get_players(self) -> List[Player]:
        with self.session as session:
            return [Player.from_orm(p) for p in session.query(PlayerORM).all()]

    def save_or_update_player(self, football_player: FootballPlayer) -> None:
        logger.info(f"saving or updating player: {football_player.football_api_id}")
        with self.session as session:
            existing_player = (
                session.query(PlayerORM).filter_by(football_api_id=football_player.football_api_id).first()
            )
            if existing_player:
                existing_player.yellow_cards = football_player.yellow_cards
                existing_player.yellow_then_red_cards = football_player.yellow_then_red_cards
                existing_player.red_cards = football_player.red_cards
                existing_player.goals = existing_player.goals
                session.add(existing_player)
            else:
                session.add(PlayerORM.from_football_player(football_player))
            session.commit()

    def save_fixture_event(self, football_fixture_event: FootballFixtureEvent) -> None:
        logger.info(f"saving fixture_event: {football_fixture_event.fixture_football_api_id}")
        with self.session as session:
            fixture_event = (
                session.query(FixtureEventORM)
                .filter(FixtureEventORM.fixture_football_api_id == football_fixture_event.fixture_football_api_id)
                .filter(FixtureEventORM.time_elapsed_min == football_fixture_event.time_elapsed_min)
                .filter(FixtureEventORM.time_elapsed_extra_min == football_fixture_event.time_elapsed_extra_min)
                .filter(FixtureEventORM.team_football_api_id == football_fixture_event.team_football_api_id)
                .filter(FixtureEventORM.player_football_api_id == football_fixture_event.player_football_api_id)
                .filter(FixtureEventORM.type == football_fixture_event.type.value)
                .filter(FixtureEventORM.detail == football_fixture_event.detail)
                .first()
            )
            if not fixture_event:
                session.add(FixtureEventORM.from_football_fixture_event(football_fixture_event))
                session.commit()

    def get_sweepstake_category(self, sweepstake_category_id: SweepstakeCategoryIDEnum) -> SweepstakeCategory:
        with self.session as session:
            sweepstake_category = session.query(SweepstakeCategoryORM).filter_by(id=sweepstake_category_id.value).one()
            return SweepstakeCategory.from_orm(sweepstake_category)

    def get_worst_team(self) -> Tuple[Team, WorstTeamData]:
        with self.session as session:
            team_to_losses = defaultdict(int)
            fixtures = session.query(FixtureORM).filter(FixtureORM.kick_off < date.today()).all()
            for fixture in fixtures:
                if fixture.home_team_won is True and fixture.away_team_won is False:
                    team_to_losses[fixture.away_team_football_api_id] += 1
                if fixture.home_team_won is False and fixture.away_team_won is True:
                    team_to_losses[fixture.home_team_football_api_id] += 1
            worst_teams_ids = [i for i, j in team_to_losses.items() if j == 3]

            worst_teams_ids_to_stats = {
                team_id: {"losses": 3, "goals_scored": 0, "goals_conceded": 0, "goal_difference": 0}
                for team_id in worst_teams_ids
            }
            for team_id in worst_teams_ids:
                losing_fixtures = (
                    session.query(FixtureORM)
                    .filter(
                        or_(
                            FixtureORM.home_team_football_api_id.in_([team_id]),
                            FixtureORM.away_team_football_api_id.in_([team_id]),
                        )
                    )
                    .all()
                )
                for fixture in losing_fixtures:
                    if fixture.home_team_football_api_id == team_id:
                        worst_teams_ids_to_stats[team_id]["goals_scored"] += fixture.home_team_goals
                        worst_teams_ids_to_stats[team_id]["goals_conceded"] += fixture.away_team_goals
                        worst_teams_ids_to_stats[team_id]["goal_difference"] += (
                            fixture.home_team_goals - fixture.away_team_goals
                        )
                    else:
                        worst_teams_ids_to_stats[team_id]["goals_scored"] += fixture.away_team_goals
                        worst_teams_ids_to_stats[team_id]["goals_conceded"] += fixture.home_team_goals
                        worst_teams_ids_to_stats[team_id]["goal_difference"] += (
                            fixture.away_team_goals - fixture.home_team_goals
                        )

            team_id_to_goal_difference = [(i, j) for i, j in worst_teams_ids_to_stats.items()]
            worst_team_id, data = sorted(
                team_id_to_goal_difference, key=lambda x: x[1]["goal_difference"], reverse=True
            ).pop()
            worst_team = session.query(TeamORM).filter_by(football_api_id=worst_team_id).one()
            return Team.from_orm(worst_team), data

    def get_filthiest_team(self) -> Tuple[Team, FilthiestTeamData]:
        with self.session as session:
            all_teams = session.query(TeamORM).all()
            team_id_to_cards = {
                team.football_api_id: {"yellow": 0, "yellow_then_red": 0, "red": 0, "total_score": 0}
                for team in all_teams
            }
            for team in all_teams:
                for player in team.players:
                    team_id_to_cards[team.football_api_id]["yellow"] += zero_if_none(player.yellow_cards)
                    team_id_to_cards[team.football_api_id]["yellow_then_red"] += zero_if_none(
                        player.yellow_then_red_cards
                    )
                    team_id_to_cards[team.football_api_id]["red"] += zero_if_none(player.red_cards)
                    team_id_to_cards[team.football_api_id]["total_score"] = (
                        (team_id_to_cards[team.football_api_id]["yellow"])
                        + (team_id_to_cards[team.football_api_id]["yellow_then_red"] * 2)
                        + (team_id_to_cards[team.football_api_id]["red"] * 3)
                    )

            team_id_to_filthy_score = [(i, j) for i, j in team_id_to_cards.items()]
            filthiest_team_id, data = sorted(team_id_to_filthy_score, key=lambda x: x[1]["total_score"]).pop()
            filthiest_team = session.query(TeamORM).filter_by(football_api_id=filthiest_team_id).one()
            return Team.from_orm(filthiest_team), data

    def get_earliest_goal(self) -> Tuple[Team, EarliestAndLatestGoalTeamData]:
        with self.session as session:
            earliest_goal = (
                session.query(FixtureEventORM)
                .filter(FixtureEventORM.type == FixtureEventTypeEnum.GOAL.value)
                .order_by(FixtureEventORM.time_elapsed_min)
                .first()
            )
            if earliest_goal.fixture.home_team_football_api_id == earliest_goal.team_football_api_id:
                against_team = earliest_goal.fixture.away_team
            else:
                against_team = earliest_goal.fixture.home_team

            data = {
                "minutes_elapsed": earliest_goal.time_elapsed_min,
                "player_full_name": earliest_goal.player.first_name + " " + earliest_goal.player.last_name,
                "against_team_name": Team.from_orm(against_team).name_and_emoji,
                "date": earliest_goal.fixture.kick_off.date(),
            }
            return Team.from_orm(earliest_goal.team), data

    def get_latest_goal(self) -> Tuple[Team, EarliestAndLatestGoalTeamData]:
        with self.session as session:
            latest_goal = (
                session.query(FixtureEventORM)
                .filter(FixtureEventORM.type == FixtureEventTypeEnum.GOAL.value)
                .filter(FixtureEventORM.time_elapsed_min == 90)
                .filter(FixtureEventORM.time_elapsed_extra_min.is_not(None))
                .order_by(FixtureEventORM.time_elapsed_extra_min.desc())
                .first()
            )
            if latest_goal.fixture.home_team_football_api_id == latest_goal.team_football_api_id:
                against_team = latest_goal.fixture.away_team
            else:
                against_team = latest_goal.fixture.home_team

            data = {
                "minutes_elapsed": latest_goal.time_elapsed_extra_min,
                "player_full_name": latest_goal.player.first_name + " " + latest_goal.player.last_name,
                "against_team_name": Team.from_orm(against_team).name_and_emoji,
                "date": latest_goal.fixture.kick_off.date(),
            }
            return Team.from_orm(latest_goal.team), data

    def get_youngest_goalscorer(self) -> Tuple[Team, YoungestAndOldestGoalScorerData]:
        with self.session as session:
            youngest_goalscorer = (
                session.query(PlayerORM)
                .filter(PlayerORM.goals.is_not(None))
                .filter(PlayerORM.goals > 0)
                .order_by(PlayerORM.date_of_birth.desc())
                .first()
            )
            age_timedelta = date.today() - youngest_goalscorer.date_of_birth
            age = f"{age_timedelta.days // 365} years and {age_timedelta.days % 365} days old"
            data = {
                "player_full_name": youngest_goalscorer.first_name + " " + youngest_goalscorer.last_name,
                "age": age,
            }
            return Team.from_orm(youngest_goalscorer.team), data

    def get_oldest_goalscorer(self) -> Tuple[Team, YoungestAndOldestGoalScorerData]:
        with self.session as session:
            oldest_goalscorer = (
                session.query(PlayerORM)
                .filter(PlayerORM.goals.is_not(None))
                .filter(PlayerORM.goals > 0)
                .order_by(PlayerORM.date_of_birth)
                .first()
            )
            age_timedelta = date.today() - oldest_goalscorer.date_of_birth
            age = f"{age_timedelta.days // 365} years and {age_timedelta.days % 365} days old"
            data = {"player_full_name": oldest_goalscorer.first_name + " " + oldest_goalscorer.last_name, "age": age}
            return Team.from_orm(oldest_goalscorer.team), data

    def get_remaining_teams(self) -> List[Team]:
        with self.session as session:
            all_remaining_teams_res = (
                session.query(FixtureORM.home_team_football_api_id, FixtureORM.away_team_football_api_id)
                .filter(FixtureORM.kick_off > datetime.utcnow())
                .all()
            )
            all_remaining_teams_ids = [item for sublist in all_remaining_teams_res for item in sublist]
            teams = session.query(TeamORM).filter(TeamORM.football_api_id.in_(all_remaining_teams_ids)).all()
            return [Team.from_orm(team) for team in teams]

    def get_non_remaining_teams(self) -> List[Team]:
        remaining_team_ids = [t.football_api_id for t in self.get_remaining_teams()]
        with self.session as session:
            teams = session.query(TeamORM).filter(TeamORM.football_api_id.not_in(remaining_team_ids)).all()
            return [Team.from_orm(team) for team in teams]
