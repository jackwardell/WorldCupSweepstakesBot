from __future__ import annotations

import os
from datetime import date
from datetime import timedelta
from functools import lru_cache
from pprint import pprint
from typing import Dict
from typing import List

import attr
import requests

from src.shared.rapid_api.models import Fixture

FIXTURE_URL = "https://api-football-v1.p.rapidapi.com/v3/fixtures"


@lru_cache
def get_football_api() -> FootballApi:
    return FootballApi()


@attr.s
class FootballApi:
    league_id: int = 1
    season: int = 2022

    headers: Dict[str, str] = {
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    @property
    def params(self) -> Dict[str, str]:
        params = {
            "league": self.league_id,
            "season": self.season,
            "from": str(date.today() + timedelta(days=1)),
            "to": str(date.today() + timedelta(days=1)),
        }
        return params

    def get_fixtures(self) -> List[Fixture]:
        response = requests.get(
            FIXTURE_URL,
            params=self.params,
            headers=self.headers
        )
        pprint(response.json())
        return [Fixture.from_response(f) for f in response.json()['response']]
