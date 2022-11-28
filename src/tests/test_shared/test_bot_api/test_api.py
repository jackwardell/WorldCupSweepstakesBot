import pytest
from src.shared.bot_api.api import BotApi


@pytest.mark.fixture
def bot_api() -> BotApi:
    return BotApi()
