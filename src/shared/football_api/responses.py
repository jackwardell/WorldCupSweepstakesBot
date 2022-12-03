from typing import List
from typing import Optional
from typing import TypedDict


class FixturesFixturesResponseFixturePeriods(TypedDict):
    first: Optional[int]
    second: Optional[int]


class FixturesFixturesResponseFixtureStatus(TypedDict):
    elapsed: Optional[int]
    long: str
    short: str


class FixturesFixturesResponseFixtureVenue(TypedDict):
    id: Optional[int]
    city: str
    name: str


class FixturesFixturesResponseFixture(TypedDict):
    id: str
    date: str
    periods: FixturesFixturesResponseFixturePeriods
    referee: Optional[str]
    status: FixturesFixturesResponseFixtureStatus
    timestamp: int
    timezone: str
    venue: FixturesFixturesResponseFixtureVenue


class FixturesFixturesResponseGoals(TypedDict):
    away: Optional[int]
    home: Optional[int]


class FixturesFixturesResponseLeague(TypedDict):
    id: int
    country: str
    flag: Optional[str]
    logo: str
    name: str
    round: str
    season: int


class FixturesFixturesResponseScorePattern(TypedDict):
    away: Optional[int]
    home: Optional[int]


class FixturesFixturesResponseScore(TypedDict):
    extratime: FixturesFixturesResponseScorePattern
    fulltime: FixturesFixturesResponseScorePattern
    halftime: FixturesFixturesResponseScorePattern
    penalty: FixturesFixturesResponseScorePattern


class FixturesFixturesResponseTeamPattern(TypedDict):
    id: int
    logo: str
    name: str
    winner: Optional[bool]


class FixturesFixturesResponseTeams(TypedDict):
    home: FixturesFixturesResponseTeamPattern
    away: FixturesFixturesResponseTeamPattern


class FixturesFixturesResponse(TypedDict):
    fixture: FixturesFixturesResponseFixture
    goals: FixturesFixturesResponseGoals
    league: FixturesFixturesResponseLeague
    score: FixturesFixturesResponseScore
    teams: FixturesFixturesResponseTeams


class TeamTeamInformationResponseTeam(TypedDict):
    id: int
    name: str
    code: str
    country: str
    founded: int
    national: bool
    logo: bool


class TeamTeamInformationResponseVenue(TypedDict):
    id: int
    name: str
    address: str
    city: str
    capacity: int
    surface: str
    image: str


class TeamTeamInformationResponse(TypedDict):
    team: TeamTeamInformationResponseTeam
    venue: TeamTeamInformationResponseVenue


class PlayerPlayerResponsePlayerBirth(TypedDict):
    date: str
    place: str
    country: str


class PlayerPlayerResponsePlayer(TypedDict):
    id: int
    name: str
    firstname: str
    lastname: str
    age: int
    birth: PlayerPlayerResponsePlayerBirth
    nationality: str
    height: str
    weight: str
    injured: bool
    photo: str


class PlayerPlayerResponseStatisticsTeam(TypedDict):
    id: str
    name: str
    logo: str


class PlayerPlayerResponseStatisticsLeague(TypedDict):
    id: Optional[int]
    name: str
    country: str
    logo: str
    flag: Optional[str]
    season: int


class PlayerPlayerResponseStatisticsGames(TypedDict):
    appearences: int
    lineups: int
    minutes: int
    number: Optional[int]
    position: str
    rating: Optional[str]
    captain: bool


class PlayerPlayerResponseStatisticsSubstitutes(TypedDict):
    in_: int
    out: int
    bench: int


class PlayerPlayerResponseStatisticsShots(TypedDict):
    total: Optional[int]
    on: Optional[int]


class PlayerPlayerResponseStatisticsShotsGoals(TypedDict):
    total: int
    conceded: int
    assists: Optional[int]
    saves: Optional[int]


class PlayerPlayerResponseStatisticsShotsPasses(TypedDict):
    total: Optional[int]
    key: Optional[int]
    accuracy: Optional[int]


class PlayerPlayerResponseStatisticsShotsTackles(TypedDict):
    total: Optional[int]
    blocks: Optional[int]
    interceptions: Optional[int]


class PlayerPlayerResponseStatisticsDuels(TypedDict):
    total: Optional[int]
    won: Optional[int]


class PlayerPlayerResponseStatisticsDribbles(TypedDict):
    attempts: Optional[int]
    success: Optional[int]
    past: Optional[int]


class PlayerPlayerResponseStatisticsFouls(TypedDict):
    drawn: Optional[int]
    committed: Optional[int]


class PlayerPlayerResponseStatisticsCards(TypedDict):
    yellow: Optional[int]
    yellowred: Optional[int]
    red: Optional[int]


class PlayerPlayerResponseStatisticsPenalty(TypedDict):
    won: Optional[int]
    commited: Optional[int]
    scored: Optional[int]
    missed: int
    saved: Optional[int]


class PlayerPlayerResponseStatistics(TypedDict):
    team: PlayerPlayerResponseStatisticsTeam
    league: PlayerPlayerResponseStatisticsLeague
    games: PlayerPlayerResponseStatisticsGames
    substitutes: PlayerPlayerResponseStatisticsSubstitutes
    shots: PlayerPlayerResponseStatisticsShots
    goals: PlayerPlayerResponseStatisticsShotsGoals
    passes: PlayerPlayerResponseStatisticsShotsPasses
    tackles: PlayerPlayerResponseStatisticsShotsTackles
    duels: PlayerPlayerResponseStatisticsDuels
    dribbles: PlayerPlayerResponseStatisticsDribbles
    fouls: PlayerPlayerResponseStatisticsFouls
    cards: PlayerPlayerResponseStatisticsCards
    penalty: PlayerPlayerResponseStatisticsPenalty


class PlayerPlayerResponse(TypedDict):
    player: PlayerPlayerResponsePlayer
    statistics: List[PlayerPlayerResponseStatistics]


class FixturesEventsResponseTime(TypedDict):
    elapsed: int
    extra: Optional[int]


class FixturesEventsResponseTeam(TypedDict):
    id: int
    name: str
    logo: str


class FixturesEventsResponsePlayer(TypedDict):
    id: int
    name: str


class FixturesEventsResponseAssist(TypedDict):
    id: int
    name: str


class FixturesEventsResponse(TypedDict):
    time: FixturesEventsResponseTime
    team: FixturesEventsResponseTeam
    player: FixturesEventsResponsePlayer
    assist: FixturesEventsResponseAssist
    type: Optional[str]
    detail: Optional[str]
    comments: Optional[str]


class FootballApiBaseResponseParameters(TypedDict):
    fixture: Optional[int]
    league: Optional[int]
    season: Optional[int]
    page: Optional[int]


class FootballApiBaseResponsePaging(TypedDict):
    current: int
    total: int


class FootballApiBaseResponse(TypedDict):
    get: str
    parameters: Optional[FootballApiBaseResponseParameters]
    errors: List[str]
    results: int
    paging: FootballApiBaseResponsePaging


class FootballApiFixtureEventsResponse(FootballApiBaseResponse):
    response: FixturesEventsResponse
