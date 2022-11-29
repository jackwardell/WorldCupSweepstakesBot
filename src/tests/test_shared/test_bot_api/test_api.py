from unittest.mock import MagicMock

import pytest
from src.shared.bot_api.api import BotApi
from src.shared.telegram_api.models import TelegramParticipant


@pytest.fixture
def bot_api() -> BotApi:
    return BotApi(telegram_api=MagicMock())


def test_save_and_get_participant(bot_api: BotApi) -> None:
    rick_participant = bot_api.save_participant(TelegramParticipant(telegram_user_id=69, first_name="Rick"))
    morty_participant = bot_api.save_participant(TelegramParticipant(telegram_user_id=420, first_name="Morty"))
    rick_and_morty_participants = bot_api.get_participants()
    assert [i.dict() for i in rick_and_morty_participants] == [rick_participant.dict(), morty_participant.dict()]
