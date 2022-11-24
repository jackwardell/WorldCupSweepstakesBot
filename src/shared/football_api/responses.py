from datetime import date
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


class PlayerResponsePlayerBirth(TypedDict):
    date: date
    place: str
    country: str


class PlayerResponsePlayer(TypedDict):
    id: int
    name: str
    firstname: str
    lastname: str
    age: int
    birth: PlayerResponsePlayerBirth
    nationality: str
    height: str
    weight: str
    injured: bool
    photo: str


class PlayerResponseStatisticsTeam(TypedDict):
    id: str
    name: str
    logo: str


class PlayerResponseStatisticsLeague(TypedDict):
    id: Optional[int]
    name: str
    country: str
    logo: str
    flag: Optional[str]
    season: int


class PlayerResponseStatisticsGames(TypedDict):
    appearences: int
    lineups: int
    minutes: int
    number: Optional[int]
    position: str
    rating: Optional[str]
    captain: bool


class PlayerResponseStatisticsSubstitutes(TypedDict):
    in_: int
    out: int
    bench: int


class PlayerResponseStatisticsShots(TypedDict):
    total: Optional[int]
    on: Optional[int]


class PlayerResponseStatisticsShotsGoals(TypedDict):
    total: int
    conceded: int
    assists: Optional[int]
    saves: Optional[int]


class PlayerResponseStatisticsShotsPasses(TypedDict):
    total: Optional[int]
    key: Optional[int]
    accuracy: Optional[int]


class PlayerResponseStatisticsShotsTackles(TypedDict):
    total: Optional[int]
    blocks: Optional[int]
    interceptions: Optional[int]


class PlayerResponseStatisticsDuels(TypedDict):
    total: Optional[int]
    won: Optional[int]


class PlayerResponseStatisticsDribbles(TypedDict):
    attempts: Optional[int]
    success: Optional[int]
    past: Optional[int]


class PlayerResponseStatisticsFouls(TypedDict):
    drawn: Optional[int]
    committed: Optional[int]


class PlayerResponseStatisticsCards(TypedDict):
    yellow: int
    yellowred: int
    red: int


class PlayerResponseStatisticsPenalty(TypedDict):
    won: Optional[int]
    commited: Optional[int]
    scored: int
    missed: int
    saved: Optional[int]


class PlayerResponseStatistics(TypedDict):
    team: PlayerResponseStatisticsTeam
    league: PlayerResponseStatisticsLeague
    games: PlayerResponseStatisticsGames
    substitutes: PlayerResponseStatisticsSubstitutes
    shots: PlayerResponseStatisticsShots
    goals: PlayerResponseStatisticsShotsGoals
    passes: PlayerResponseStatisticsShotsPasses
    tackles: PlayerResponseStatisticsShotsTackles
    duels: PlayerResponseStatisticsDuels
    dribbles: PlayerResponseStatisticsDribbles
    fouls: PlayerResponseStatisticsFouls
    cards: PlayerResponseStatisticsCards
    penalty: PlayerResponseStatisticsPenalty


class PlayerResponse(TypedDict):
    player: PlayerResponsePlayer
    statistics: PlayerResponseStatistics
