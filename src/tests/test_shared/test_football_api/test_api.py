from unittest.mock import MagicMock

import pytest
import requests
from src.shared.football_api.api import FootballApi


@pytest.fixture
def football_api() -> FootballApi:
    return FootballApi()


def test_get_fixtures(football_api: FootballApi) -> None:
    requests.get = MagicMock(
        return_value={
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
        }
    )
    # football_api.
