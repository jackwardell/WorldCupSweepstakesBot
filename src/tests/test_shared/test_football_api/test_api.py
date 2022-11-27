import datetime
from unittest.mock import MagicMock

import pytest
import responses
from src.shared.football_api.api import FootballApi
from src.shared.football_api.models import FootballFixture


@pytest.fixture
def football_api() -> FootballApi:
    return FootballApi()


@pytest.fixture
def response() -> MagicMock:
    return MagicMock()


@pytest.mark.parametrize("today_only", [True, False])
@responses.activate
def test_get_fixtures(football_api: FootballApi, today_only: bool, response: MagicMock) -> None:
    responses.get(
        "https://api-football-v1.p.rapidapi.com/v3/fixtures",
        json={
            "get": "fixtures",
            "parameters": {"league": "1", "from": "2022-11-25", "to": "2022-11-25", "season": "2022"},
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
