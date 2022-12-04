from __future__ import annotations

import time
from datetime import date
from functools import lru_cache
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import attr
import requests
from src.shared.config import get_config
from src.shared.football_api.models import FootballFixture
from src.shared.football_api.models import FootballFixtureEvent
from src.shared.football_api.models import FootballPlayer
from src.shared.football_api.models import FootballTeam


@lru_cache
def get_football_api() -> FootballApi:
    return FootballApi()


def get_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "X-RapidAPI-Key": get_config().RAPID_API_KEY,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com",
        }
    )
    return session


@attr.s
class FootballApi:
    league_id: str = "1"
    season: str = "2022"
    session: requests.Session = attr.ib(factory=get_session)

    def get(self, url: str, params: Dict[str, Union[str, int]]) -> Dict[str, Any]:
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def get_fixtures(self, today_only: bool = True) -> List[FootballFixture]:
        params = {"league": self.league_id, "season": self.season}
        if today_only:
            params["from"] = str(date.today())
            params["to"] = str(date.today())
        response = self.get(
            "https://api-football-v1.p.rapidapi.com/v3/fixtures",
            params=params,
        )
        return [FootballFixture.from_football_api_response(f) for f in response["response"]]

    def get_teams(self) -> List[FootballTeam]:
        params = {"league": self.league_id, "season": self.season}
        response = self.get(
            "https://api-football-v1.p.rapidapi.com/v3/teams",
            params=params,
        )
        return [FootballTeam.from_football_api_response(t) for t in response["response"]]

    def get_players(self, page: Optional[int] = None) -> List[FootballPlayer]:
        params = {"league": self.league_id, "season": self.season}
        if page:
            params["page"] = page
        response = self.get(
            "https://api-football-v1.p.rapidapi.com/v3/players",
            params=params,
        )
        return [FootballPlayer.from_football_api_response(p) for p in response["response"]]

    def get_all_players(self) -> List[FootballPlayer]:
        current_page = 1
        end_page = 1_000_000
        players = []
        while current_page <= end_page:
            params = {"league": self.league_id, "season": self.season, "page": current_page}
            response = self.get(
                "https://api-football-v1.p.rapidapi.com/v3/players",
                params=params,
            )
            end_page = response["paging"]["total"]
            players.extend([FootballPlayer.from_football_api_response(p) for p in response["response"]])
            current_page += 1
            time.sleep(2)
        return players

    def get_fixture_events(self, fixture_football_api_id: int) -> List[FootballFixtureEvent]:
        params = {"fixture": fixture_football_api_id}
        response = self.get(
            "https://api-football-v1.p.rapidapi.com/v3/fixtures/events",
            params=params,
        )
        return [
            FootballFixtureEvent.from_football_api_response(fixture_football_api_id, e) for e in response["response"]
        ]
