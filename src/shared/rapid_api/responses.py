from typing import Optional
from typing import TypedDict


class FixturesPeriodsResponse(TypedDict):
    first: Optional[int]
    second: Optional[int]


class FixturesStatusResponse(TypedDict):
    elapsed: Optional[int]
    long: str
    short: str


class FixtureVenueResponse(TypedDict):
    id: Optional[int]
    city: str
    name: str


class FixtureResponse(TypedDict):
    id: str
    date: str
    periods: FixturesPeriodsResponse
    referee: Optional[str]
    status: FixturesStatusResponse
    timestamp: int
    timezone: str
    venue: FixtureVenueResponse


class GoalsResponse(TypedDict):
    away: Optional[int]
    home: Optional[int]


class LeagueResponse(TypedDict):
    id: int
    country: str
    flag: Optional[str]
    logo: str
    name: str
    round: str
    season: int


class SubScoreResponse(TypedDict):
    away: Optional[int]
    home: Optional[int]


class ScoreResponse(TypedDict):
    extratime: SubScoreResponse
    fulltime: SubScoreResponse
    halftime: SubScoreResponse
    penalty: SubScoreResponse


class SubTeamResponse(TypedDict):
    id: int
    logo: str
    name: str
    winner: Optional[bool]


class TeamsResponse(TypedDict):
    home: SubTeamResponse
    away: SubTeamResponse


class TotalFixtureResponse(TypedDict):
    fixture: FixtureResponse
    goals: GoalsResponse
    league: LeagueResponse
    score: ScoreResponse
    teams: TeamsResponse
