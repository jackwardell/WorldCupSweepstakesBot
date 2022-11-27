from __future__ import annotations

from datetime import date
from functools import lru_cache
from typing import Dict
from typing import List
from typing import Optional

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


@attr.s
class FootballApi:
    league_id: str = "1"
    season: str = "2022"

    @property
    def headers(self) -> Dict[str, str]:
        return {"X-RapidAPI-Key": get_config().RAPID_API_KEY, "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"}

    @property
    def fixtures_url(self) -> str:
        return "https://api-football-v1.p.rapidapi.com/v3/fixtures"

    @property
    def teams_url(self) -> str:
        return "https://api-football-v1.p.rapidapi.com/v3/teams"

    @property
    def players_url(self) -> str:
        return "https://api-football-v1.p.rapidapi.com/v3/players"

    @property
    def fixture_events_url(self) -> str:
        return "https://api-football-v1.p.rapidapi.com/v3/fixtures/events"

    def get_fixtures(self, today_only: bool = True) -> List[FootballFixture]:
        params = {"league": self.league_id, "season": self.season}
        if today_only:
            params["from"] = str(date.today())
            params["to"] = str(date.today())
        response = requests.get(
            self.fixtures_url,
            params=params,
            headers=self.headers,
        )
        return [FootballFixture.from_football_api_response(f) for f in response.json()["response"]]

    def get_teams(self) -> List[FootballTeam]:
        params = {"league": self.league_id, "season": self.season}
        response = requests.get(
            self.teams_url,
            params=params,
            headers=self.headers,
        )
        return [FootballTeam.from_football_api_response(t) for t in response.json()["response"]]

    def get_players(self, page: Optional[int] = None) -> List[FootballPlayer]:
        params = {"league": self.league_id, "season": self.season}
        if page:
            params["page"] = page
        response = requests.get(
            self.players_url,
            params=params,
            headers=self.headers,
        )
        return [FootballPlayer.from_football_api_response(p) for p in response.json()["response"]]

    def get_fixture_events(self, fixture_football_api_key: int) -> List[FootballFixtureEvent]:
        params = {"fixture": fixture_football_api_key}
        response = requests.get(
            self.fixture_events_url,
            params=params,
            headers=self.headers,
        )
        return [FootballFixtureEvent.from_football_api_response(e) for e in response.json()["response"]]

    # def get_all_players(self, sleep_per_call: Optional[int] = None) -> List[FootballPlayer]:
    #     params = self.get_params()
    #     params['page'] = 1
    #     response = requests.get(
    #         self.players_url,
    #         params=params,
    #         headers=self.headers,
    #     )
    #     players = [FootballPlayer.from_response(p) for p in response.json()['response']]
    #     number_of_pages = response.json()["paging"]["total"]
    #     for page in range(2, number_of_pages + 1):
    #         params['page'] = page
    #         response = requests.get(
    #             self.players_url,
    #             params=params,
    #             headers=self.headers,
    #         )
    #         response.raise_for_status()
    #         players.extend([FootballPlayer.from_response(p) for p in response.json()["response"]])
    #         if sleep_per_call:
    #             time.sleep(sleep_per_call)
    #     assert (
    #             response.json()["paging"]["current"] == number_of_pages
    #     ), f"{response.json()['paging']['current']} != {number_of_pages}"
    #     return players
