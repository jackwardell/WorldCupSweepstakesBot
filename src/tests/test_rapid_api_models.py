from typing import Any
from typing import Dict

import pytest


@pytest.fixture
def response() -> Dict[str, Any]:
    return {
        "errors": [],
        "get": "fixtures",
        "paging": {"current": 1, "total": 1},
        "parameters": {
            "from": "2022-11-20",
            "league": "1",
            "season": "2022",
            "to": "2022-11-20",
        },
        "response": [
            {
                "fixture": {
                    "date": "2022-11-20T16:00:00+00:00",
                    "id": 855736,
                    "periods": {"first": None, "second": None},
                    "referee": None,
                    "status": {"elapsed": None, "long": "Not Started", "short": "NS"},
                    "timestamp": 1668960000,
                    "timezone": "UTC",
                    "venue": {"city": "Al Khor", "id": None, "name": "Al Bayt Stadium"},
                },
                "goals": {"away": None, "home": None},
                "league": {
                    "country": "World",
                    "flag": None,
                    "id": 1,
                    "logo": "https://media.api-sports.io/football/leagues/1.png",
                    "name": "World Cup",
                    "round": "Group Stage - 1",
                    "season": 2022,
                },
                "score": {
                    "extratime": {"away": None, "home": None},
                    "fulltime": {"away": None, "home": None},
                    "halftime": {"away": None, "home": None},
                    "penalty": {"away": None, "home": None},
                },
                "teams": {
                    "away": {
                        "id": 2382,
                        "logo": "https://media.api-sports.io/football/teams/2382.png",
                        "name": "Ecuador",
                        "winner": None,
                    },
                    "home": {
                        "id": 1569,
                        "logo": "https://media.api-sports.io/football/teams/1569.png",
                        "name": "Qatar",
                        "winner": None,
                    },
                },
            }
        ],
        "results": 1,
    }
