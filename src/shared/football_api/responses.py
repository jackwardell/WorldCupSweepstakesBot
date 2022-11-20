from typing import Optional
from typing import TypedDict


class FixturesResponseFixturePeriods(TypedDict):
    first: Optional[int]
    second: Optional[int]


class FixturesResponseFixtureStatus(TypedDict):
    elapsed: Optional[int]
    long: str
    short: str


class FixtureResponseFixtureVenue(TypedDict):
    id: Optional[int]
    city: str
    name: str


class FixtureResponseFixture(TypedDict):
    id: str
    date: str
    periods: FixturesResponseFixturePeriods
    referee: Optional[str]
    status: FixturesResponseFixtureStatus
    timestamp: int
    timezone: str
    venue: FixtureResponseFixtureVenue


class FixtureResponseGoals(TypedDict):
    away: Optional[int]
    home: Optional[int]


class FixtureResponseLeague(TypedDict):
    id: int
    country: str
    flag: Optional[str]
    logo: str
    name: str
    round: str
    season: int


class FixtureResponseScorePattern(TypedDict):
    away: Optional[int]
    home: Optional[int]


class FixtureResponseScore(TypedDict):
    extratime: FixtureResponseScorePattern
    fulltime: FixtureResponseScorePattern
    halftime: FixtureResponseScorePattern
    penalty: FixtureResponseScorePattern


class FixtureResponseTeamPattern(TypedDict):
    id: int
    logo: str
    name: str
    winner: Optional[bool]


class FixtureResponseTeams(TypedDict):
    home: FixtureResponseTeamPattern
    away: FixtureResponseTeamPattern


class FixtureResponse(TypedDict):
    fixture: FixtureResponseFixture
    goals: FixtureResponseGoals
    league: FixtureResponseLeague
    score: FixtureResponseScore
    teams: FixtureResponseTeams


class TeamResponseTeam(TypedDict):
    id: int
    name: str
    code: str
    country: str
    founded: int
    national: bool
    logo: bool


class TeamResponseVenue(TypedDict):
    id: int
    name: str
    address: str
    city: str
    capacity: int
    surface: str
    image: str


class TeamResponse(TypedDict):
    team: TeamResponseTeam
    venue: TeamResponseVenue
