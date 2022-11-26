import pytest
from src.shared.football_api.api import FootballApi


@pytest.fixture
def football_api() -> FootballApi:
    return FootballApi()
