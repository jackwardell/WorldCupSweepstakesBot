from __future__ import annotations

from datetime import date
from functools import lru_cache
from typing import Dict
from typing import List

import attr
import requests
from src.shared.config import get_config
from src.shared.football_api.models import FootballFixture
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

    def get_fixtures(self, today_only: bool = True) -> List[FootballFixture]:
        params = {
            "league": self.league_id,
            "season": self.season,
        }
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
            params={"league": self.league_id, "season": self.season},
            headers=self.headers,
        )
        return [FootballTeam.from_response(t) for t in response.json()["response"]]
