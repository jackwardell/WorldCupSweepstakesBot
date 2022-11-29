import pytest
from src.shared.bot_api.api import BotApi


@pytest.fixture
def bot_api() -> BotApi:
    return BotApi()


def test_get_participants(bot_api: BotApi) -> None:
    bot_api.get_participants()
