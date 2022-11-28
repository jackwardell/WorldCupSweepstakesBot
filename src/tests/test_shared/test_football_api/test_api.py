import datetime
from typing import Optional

import pytest
import responses
from src.shared.football_api.api import FootballApi
from src.shared.football_api.models import FootballFixture
from src.shared.football_api.models import FootballFixtureEvent
from src.shared.football_api.models import FootballPlayer
from src.shared.football_api.models import FootballTeam
from src.shared.schemas import FixtureEventType


@pytest.fixture
def football_api() -> FootballApi:
    return FootballApi()


@pytest.mark.parametrize("today_only", [True, False])
@responses.activate
def test_get_fixtures(football_api: FootballApi, today_only: bool) -> None:
    params = {"league": "1", "season": "2022"}
    if today_only:
        params["from"] = str(datetime.date.today())
        params["to"] = str(datetime.date.today())
    route = responses.get(
        "https://api-football-v1.p.rapidapi.com/v3/fixtures",
        json={
            "get": "fixtures",
            "parameters": params,
            "errors": [],
            "results": 4,
            "paging": {"current": 1, "total": 1},
            "response": [
                {
                    "fixture": {
                        "id": 866682,
                        "referee": "Mario Escobar, Guatemala",
                        "timezone": "UTC",
                        "date": "2022-11-25T10:00:00+00:00",
                        "timestamp": 1669370400,
                        "periods": {"first": 1669370400, "second": 1669374000},
                        "venue": {"id": None, "name": "Ahmed bin Ali Stadium", "city": "Al Rayyan"},
                        "status": {"long": "Match Finished", "short": "FT", "elapsed": 90},
                    },
                    "league": {
                        "id": 1,
                        "name": "World Cup",
                        "country": "World",
                        "logo": "https://media.api-sports.io/football/leagues/1.png",
                        "flag": None,
                        "season": 2022,
                        "round": "Group Stage - 2",
                    },
                    "teams": {
                        "home": {
                            "id": 767,
                            "name": "Wales",
                            "logo": "https://media.api-sports.io/football/teams/767.png",
                            "winner": False,
                        },
                        "away": {
                            "id": 22,
                            "name": "Iran",
                            "logo": "https://media.api-sports.io/football/teams/22.png",
                            "winner": True,
                        },
                    },
                    "goals": {"home": 0, "away": 2},
                    "score": {
                        "halftime": {"home": 0, "away": 0},
                        "fulltime": {"home": 0, "away": 2},
                        "extratime": {"home": None, "away": None},
                        "penalty": {"home": None, "away": None},
                    },
                },
                {
                    "fixture": {
                        "id": 855747,
                        "referee": "Antonio Mateu, Spain",
                        "timezone": "UTC",
                        "date": "2022-11-25T13:00:00+00:00",
                        "timestamp": 1669381200,
                        "periods": {"first": 1669381200, "second": 1669384800},
                        "venue": {"id": None, "name": "Al-Thumama Stadium", "city": "Al-Thumama"},
                        "status": {"long": "Match Finished", "short": "FT", "elapsed": 90},
                    },
                    "league": {
                        "id": 1,
                        "name": "World Cup",
                        "country": "World",
                        "logo": "https://media.api-sports.io/football/leagues/1.png",
                        "flag": None,
                        "season": 2022,
                        "round": "Group Stage - 2",
                    },
                    "teams": {
                        "home": {
                            "id": 1569,
                            "name": "Qatar",
                            "logo": "https://media.api-sports.io/football/teams/1569.png",
                            "winner": False,
                        },
                        "away": {
                            "id": 13,
                            "name": "Senegal",
                            "logo": "https://media.api-sports.io/football/teams/13.png",
                            "winner": True,
                        },
                    },
                    "goals": {"home": 1, "away": 3},
                    "score": {
                        "halftime": {"home": 0, "away": 1},
                        "fulltime": {"home": 1, "away": 3},
                        "extratime": {"home": None, "away": None},
                        "penalty": {"home": None, "away": None},
                    },
                },
            ],
        },
    )
    football_fixtures = football_api.get_fixtures(today_only=today_only)
    assert football_fixtures == [
        FootballFixture(
            football_api_id=866682,
            home_team_football_api_id=767,
            away_team_football_api_id=22,
            home_team_goals=0,
            away_team_goals=2,
            home_team_winner=False,
            away_team_winner=True,
            kick_off=datetime.datetime(2022, 11, 25, 10, 0, tzinfo=datetime.timezone.utc),
            venue_city="Al Rayyan",
            venue_name="Ahmed bin Ali Stadium",
            round="Group Stage - 2",
            home_goals_halftime=0,
            away_goals_halftime=0,
            home_goals_fulltime=0,
            away_goals_fulltime=2,
            away_goals_extratime=None,
            home_goals_extratime=None,
            home_goals_penalties=None,
            away_goals_penalties=None,
        ),
        FootballFixture(
            football_api_id=855747,
            home_team_football_api_id=1569,
            away_team_football_api_id=13,
            home_team_goals=1,
            away_team_goals=3,
            home_team_winner=False,
            away_team_winner=True,
            kick_off=datetime.datetime(2022, 11, 25, 13, 0, tzinfo=datetime.timezone.utc),
            venue_city="Al-Thumama",
            venue_name="Al-Thumama Stadium",
            round="Group Stage - 2",
            home_goals_halftime=0,
            away_goals_halftime=1,
            home_goals_fulltime=1,
            away_goals_fulltime=3,
            away_goals_extratime=None,
            home_goals_extratime=None,
            home_goals_penalties=None,
            away_goals_penalties=None,
        ),
    ]
    assert route.call_count == 1
    if today_only:
        assert responses.calls[0].request.params == {
            "league": "1",
            "season": "2022",
            "to": str(datetime.date.today()),
            "from": str(datetime.date.today()),
        }
    else:
        assert responses.calls[0].request.params == {"league": "1", "season": "2022"}
    assert responses.calls[0].request.headers["X-RapidAPI-Key"] == "test3"
    assert responses.calls[0].request.headers["X-RapidAPI-Host"] == "api-football-v1.p.rapidapi.com"


@responses.activate
def test_get_teams(football_api: FootballApi) -> None:
    route = responses.get(
        "https://api-football-v1.p.rapidapi.com/v3/teams",
        json={
            "get": "teams",
            "parameters": {"league": "1", "season": "2022"},
            "errors": [],
            "results": 4,
            "paging": {"current": 1, "total": 1},
            "response": [
                {
                    "team": {
                        "id": 2382,
                        "name": "Ecuador",
                        "code": "ECU",
                        "country": "Ecuador",
                        "founded": 1925,
                        "national": True,
                        "logo": "https://media.api-sports.io/football/teams/2382.png",
                    },
                    "venue": {
                        "id": 465,
                        "name": "Estadio Olímpico Atahualpa",
                        "address": "Avenida 6 de Diciembre y Avenida Naciones Unidas",
                        "city": "Quito",
                        "capacity": 40958,
                        "surface": "grass",
                        "image": "https://media.api-sports.io/football/venues/465.png",
                    },
                },
                {
                    "team": {
                        "id": 2384,
                        "name": "USA",
                        "code": "USA",
                        "country": "USA",
                        "founded": 1913,
                        "national": True,
                        "logo": "https://media.api-sports.io/football/teams/2384.png",
                    },
                    "venue": {
                        "id": 2855,
                        "name": "Robert F. Kennedy Memorial Stadium",
                        "address": "2400 East Capitol Street Southeast",
                        "city": "Washington, District of Columbia",
                        "capacity": 56692,
                        "surface": "grass",
                        "image": "https://media.api-sports.io/football/venues/2855.png",
                    },
                },
            ],
        },
    )
    football_teams = football_api.get_teams()
    assert football_teams == [
        FootballTeam(
            football_api_id=2382,
            name="Ecuador",
        ),
        FootballTeam(
            football_api_id=2384,
            name="USA",
        ),
    ]
    assert route.call_count == 1
    assert responses.calls[0].request.params == {"league": "1", "season": "2022"}
    assert responses.calls[0].request.headers["X-RapidAPI-Key"] == "test3"
    assert responses.calls[0].request.headers["X-RapidAPI-Host"] == "api-football-v1.p.rapidapi.com"


@pytest.mark.parametrize("page", [None, 2])
@responses.activate
def test_get_players(football_api: FootballApi, page: Optional[int]) -> None:
    route = responses.get(
        "https://api-football-v1.p.rapidapi.com/v3/players",
        json={
            "get": "teams",
            "parameters": {"league": "1", "season": "2022"},
            "errors": [],
            "results": 4,
            "paging": {"current": 1, "total": 1},
            "response": [
                {
                    "player": {
                        "id": 44843,
                        "name": "M. Boyle",
                        "firstname": "Martin Callie",
                        "lastname": "Boyle",
                        "age": 29,
                        "birth": {"date": "1993-04-25", "place": "Aberdeen", "country": "Scotland"},
                        "nationality": "Australia",
                        "height": "172 cm",
                        "weight": "66 kg",
                        "injured": False,
                        "photo": "https://media.api-sports.io/football/players/44843.png",
                    },
                    "statistics": [
                        {
                            "team": {
                                "id": 20,
                                "name": "Australia",
                                "logo": "https://media.api-sports.io/football/teams/20.png",
                            },
                            "league": {
                                "id": 1,
                                "name": "World Cup",
                                "country": "World",
                                "logo": "https://media.api-sports.io/football/leagues/1.png",
                                "flag": None,
                                "season": 2022,
                            },
                            "games": {
                                "appearences": 0,
                                "lineups": 0,
                                "minutes": 0,
                                "number": None,
                                "position": "Attacker",
                                "rating": None,
                                "captain": False,
                            },
                            "substitutes": {"in": 0, "out": 0, "bench": 0},
                            "shots": {"total": None, "on": None},
                            "goals": {"total": 1, "conceded": None, "assists": None, "saves": None},
                            "passes": {"total": None, "key": None, "accuracy": None},
                            "tackles": {"total": None, "blocks": None, "interceptions": None},
                            "duels": {"total": None, "won": None},
                            "dribbles": {"attempts": None, "success": None, "past": None},
                            "fouls": {"drawn": None, "committed": None},
                            "cards": {"yellow": 1, "yellowred": 2, "red": 3},
                            "penalty": {"won": None, "commited": None, "scored": None, "missed": None, "saved": None},
                        }
                    ],
                },
                {
                    "player": {
                        "id": 152654,
                        "name": "J. Frimpong",
                        "firstname": "Jeremie",
                        "lastname": "Agyekum Frimpong",
                        "age": 22,
                        "birth": {"date": "2000-12-10", "place": "Amsterdam", "country": "Netherlands"},
                        "nationality": "Netherlands",
                        "height": "171 cm",
                        "weight": "63 kg",
                        "injured": False,
                        "photo": "https://media.api-sports.io/football/players/152654.png",
                    },
                    "statistics": [
                        {
                            "team": {
                                "id": 1118,
                                "name": "Netherlands",
                                "logo": "https://media.api-sports.io/football/teams/1118.png",
                            },
                            "league": {
                                "id": 1,
                                "name": "World Cup",
                                "country": "World",
                                "logo": "https://media.api-sports.io/football/leagues/1.png",
                                "flag": None,
                                "season": 2022,
                            },
                            "games": {
                                "appearences": 0,
                                "lineups": 0,
                                "minutes": 0,
                                "number": None,
                                "position": "Defender",
                                "rating": None,
                                "captain": False,
                            },
                            "substitutes": {"in": 0, "out": 0, "bench": 2},
                            "shots": {"total": None, "on": None},
                            "goals": {"total": 0, "conceded": 0, "assists": None, "saves": None},
                            "passes": {"total": None, "key": None, "accuracy": None},
                            "tackles": {"total": None, "blocks": None, "interceptions": None},
                            "duels": {"total": None, "won": None},
                            "dribbles": {"attempts": None, "success": None, "past": None},
                            "fouls": {"drawn": None, "committed": None},
                            "cards": {"yellow": 0, "yellowred": 0, "red": 0},
                            "penalty": {"won": None, "commited": None, "scored": 0, "missed": 0, "saved": None},
                        }
                    ],
                },
            ],
        },
    )
    football_players = football_api.get_players()
    assert football_players == [
        FootballPlayer(
            football_api_id=44843,
            first_name="Martin Callie",
            last_name="Boyle",
            date_of_birth=datetime.date.fromisoformat("1993-04-25"),
            team_football_api_id=20,
            yellow_cards=1,
            yellow_then_red_cards=2,
            red_cards=3,
            goals=1,
        ),
        FootballPlayer(
            football_api_id=152654,
            first_name="Jeremie",
            last_name="Agyekum Frimpong",
            date_of_birth=datetime.date.fromisoformat("2000-12-10"),
            team_football_api_id=1118,
            yellow_cards=0,
            yellow_then_red_cards=0,
            red_cards=0,
            goals=0,
        ),
    ]
    assert route.call_count == 1
    assert responses.calls[0].request.params == {"league": "1", "season": "2022"}
    assert responses.calls[0].request.headers["X-RapidAPI-Key"] == "test3"
    assert responses.calls[0].request.headers["X-RapidAPI-Host"] == "api-football-v1.p.rapidapi.com"


@responses.activate
def test_get_fixture_events(football_api: FootballApi) -> None:
    route = responses.get(
        "https://api-football-v1.p.rapidapi.com/v3/fixtures/events",
        json={
            "get": "fixtures/events",
            "parameters": {"fixture": "11111"},
            "errors": [],
            "results": 11,
            "paging": {"current": 1, "total": 1},
            "response": [
                {
                    "time": {"elapsed": 11, "extra": None},
                    "team": {
                        "id": 163,
                        "name": "Borussia Monchengladbach",
                        "logo": "https://media.api-sports.io/football/teams/163.png",
                    },
                    "player": {"id": 25637, "name": "C. Kramer"},
                    "assist": {"id": 25630, "name": "T. Jantschke"},
                    "type": "subst",
                    "detail": "Substitution 1",
                    "comments": None,
                },
                {
                    "time": {"elapsed": 31, "extra": None},
                    "team": {
                        "id": 157,
                        "name": "Bayern Munich",
                        "logo": "https://media.api-sports.io/football/teams/157.png",
                    },
                    "player": {"id": 519, "name": "Corentin Tolisso"},
                    "assist": {"id": None, "name": None},
                    "type": "Card",
                    "detail": "Yellow Card",
                    "comments": None,
                },
                {
                    "time": {"elapsed": 90, "extra": 1},
                    "team": {
                        "id": 163,
                        "name": "Borussia Monchengladbach",
                        "logo": "https://media.api-sports.io/football/teams/163.png",
                    },
                    "player": {"id": 2929, "name": "T. Hazard"},
                    "assist": {"id": None, "name": None},
                    "type": "Goal",
                    "detail": "Penalty",
                    "comments": None,
                },
            ],
        },
    )
    football_fixture_events = football_api.get_fixture_events(fixture_football_api_key=11111)
    assert football_fixture_events == [
        FootballFixtureEvent(
            time_elapsed_min=11,
            time_elapsed_extra_min=None,
            team_football_api_id=163,
            player_football_api_id=25637,
            type=FixtureEventType.SUBST,
            detail="Substitution 1",
        ),
        FootballFixtureEvent(
            time_elapsed_min=31,
            time_elapsed_extra_min=None,
            team_football_api_id=157,
            player_football_api_id=519,
            type=FixtureEventType.CARD,
            detail="Yellow Card",
        ),
        FootballFixtureEvent(
            time_elapsed_min=90,
            time_elapsed_extra_min=1,
            team_football_api_id=163,
            player_football_api_id=2929,
            type=FixtureEventType.GOAL,
            detail="Penalty",
        ),
    ]
    assert route.call_count == 1
    assert responses.calls[0].request.params == {"fixture": "11111"}
    assert responses.calls[0].request.headers["X-RapidAPI-Key"] == "test3"
    assert responses.calls[0].request.headers["X-RapidAPI-Host"] == "api-football-v1.p.rapidapi.com"
