from typing import List
from unittest.mock import MagicMock

import pytest
from src.shared.bot_api.api import BotApi
from src.shared.bot_api.db import TeamDrawnByParticipantORM
from src.shared.football_api.models import FootballTeam
from src.shared.telegram_api.models import TelegramParticipant


@pytest.fixture
def bot_api() -> BotApi:
    return BotApi(telegram_api=MagicMock())


@pytest.mark.parametrize(
    "telegram_participants",
    [
        [
            TelegramParticipant(telegram_user_id=69, first_name="Rick"),
        ],
        [
            TelegramParticipant(telegram_user_id=69, first_name="Rick"),
            TelegramParticipant(telegram_user_id=420, first_name="Morty"),
        ],
    ],
)
def test_save_and_get_participant(bot_api: BotApi, telegram_participants: List[TelegramParticipant]) -> None:
    for telegram_participant in telegram_participants:
        bot_api.save_participant(telegram_participant)
    participants = bot_api.get_participants()
    assert [i.dict() for i in telegram_participants] == [i.dict() for i in participants]


@pytest.mark.parametrize(
    "football_teams",
    [
        [
            FootballTeam(football_api_id=1, name="England"),
        ],
        [
            FootballTeam(football_api_id=1, name="England"),
            FootballTeam(football_api_id=2, name="France"),
        ],
    ],
)
def test_save_and_get_team(bot_api: BotApi, football_teams: List[FootballTeam]) -> None:
    for football_team in football_teams:
        bot_api.save_team(football_team)
    teams = bot_api.get_teams()
    # exclude_none as we don't want {'participant': None} in the dict
    assert [i.dict() for i in football_teams] == [i.dict(exclude_none=True) for i in teams]


def test_save_team_drawn_by_participant(bot_api: BotApi) -> None:
    football_team = FootballTeam(football_api_id=1, name="England")
    telegram_participant = TelegramParticipant(telegram_user_id=69, first_name="Rick")
    bot_api.save_team(football_team)
    bot_api.save_participant(telegram_participant)
    bot_api.save_team_drawn_by_participant(football_team.football_api_id, telegram_participant.telegram_user_id)
    with bot_api.session as session:
        res = session.query(TeamDrawnByParticipantORM).one()
        assert res.team_football_api_id == football_team.football_api_id
        assert res.participant_telegram_user_id == telegram_participant.telegram_user_id
