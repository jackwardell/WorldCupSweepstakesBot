from datetime import date
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class FixtureEventTypeEnum(Enum):
    CARD = "Card"
    GOAL = "Goal"
    SUBST = "subst"
    VAR = "Var"


class SweepstakeCategoryIDEnum(Enum):
    WINNING_TEAM = 1
    WORST_TEAM = 2
    MOST_MEANINGFUL_PROTEST = 3
    FILTHIEST_TEAM = 4
    EARLIEST_GOAL = 5
    LATEST_GOAL = 6
    OLDEST_GOAL_SCORER = 7
    YOUNGEST_GOAL_SCORER = 8


class SweepstakeCategorySchema(BaseModel):
    id: SweepstakeCategoryIDEnum
    name: str
    reward_amount: int


class ParticipantSchema(BaseModel):
    telegram_user_id: int
    first_name: str


class TeamSchema(BaseModel):
    football_api_id: int
    name: str


class FixtureSchema(BaseModel):
    football_api_id: int
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


class PlayerSchema(BaseModel):
    football_api_id: int
    first_name: str
    last_name: str
    date_of_birth: date
    team_football_api_id: int
    yellow_cards: Optional[int]
    yellow_then_red_cards: Optional[int]
    red_cards: Optional[int]
    goals: Optional[int]


class FixtureEventSchema(BaseModel):
    fixture_football_api_id: int
    time_elapsed_min: int
    time_elapsed_extra_min: Optional[int]
    team_football_api_id: int
    player_football_api_id: int
    type: FixtureEventTypeEnum
    detail: str
