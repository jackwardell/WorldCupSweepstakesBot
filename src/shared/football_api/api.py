from __future__ import annotations

from datetime import date
from functools import lru_cache
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import attr
import requests
from src.shared.config import get_config
from src.shared.football_api.models import FootballFixture
from src.shared.football_api.models import FootballPlayer
from src.shared.football_api.models import FootballTeam


@lru_cache
def get_football_api() -> FootballApi:
    return FootballApi()


@attr.s
class FootballApi:
    league_id: int = 1
    season: int = 2022

    headers: Dict[str, str] = {
        "X-RapidAPI-Key": get_config().RAPID_API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com",
    }

    @property
    def fixtures_url(self) -> str:
        return "https://api-football-v1.p.rapidapi.com/v3/fixtures"

    @property
    def teams_url(self) -> str:
        return "https://api-football-v1.p.rapidapi.com/v3/teams"

    @property
    def players_url(self) -> str:
        return "https://api-football-v1.p.rapidapi.com/v3/players"

    def get_params(self) -> Dict[str, Union[int, str]]:
        return {"league": self.league_id, "season": self.season}

    def get_fixtures(self, today_only: bool = True) -> List[FootballFixture]:
        params = self.get_params()
        if today_only:
            params["from"] = str(date.today())
            params["to"] = str(date.today())
        response = requests.get(
            self.fixtures_url,
            params=params,
            headers=self.headers,
        )
        return [FootballFixture.from_response(f) for f in response.json()["response"]]

    def get_teams(self) -> List[FootballTeam]:
        response = requests.get(
            self.teams_url,
            params=self.get_params(),
            headers=self.headers,
        )
        return [FootballTeam.from_response(t) for t in response.json()["response"]]

    def get_players(self, page: Optional[int] = None) -> List[FootballPlayer]:
        params = self.get_params()
        if page:
            params["page"] = page
        response = requests.get(
            self.players_url,
            params=params,
            headers=self.headers,
        )
        return [FootballPlayer.from_response(p) for p in response.json()["response"]]

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
