from typing import List
from unittest.mock import MagicMock

import pytest
from src.shared.bot_api.api import BotApi
from src.shared.bot_api.db import TeamDrawnByParticipantORM
from src.shared.bot_api.models import Participant
from src.shared.bot_api.models import Team
from src.shared.football_api.models import FootballTeam
from src.shared.telegram_api.models import TelegramParticipant


@pytest.fixture
def bot_api() -> BotApi:
    return BotApi(telegram_api=MagicMock())


@pytest.mark.parametrize(
    "input_telegram_participants, output_participants",
    [
        (
            [TelegramParticipant(telegram_user_id=69, first_name="Rick")],
            [Participant(telegram_user_id=69, first_name="Rick")],
        ),
        (
            [
                TelegramParticipant(telegram_user_id=69, first_name="Rick"),
                TelegramParticipant(telegram_user_id=420, first_name="Morty"),
            ],
            [
                Participant(telegram_user_id=69, first_name="Rick"),
                Participant(telegram_user_id=420, first_name="Morty"),
            ],
        ),
    ],
)
def test_save_and_get_participant(
    bot_api: BotApi,
    input_telegram_participants: List[TelegramParticipant],
    output_participants: List[Participant],
) -> None:
    for telegram_participant in input_telegram_participants:
        bot_api.save_participant(telegram_participant)
    participants = bot_api.get_participants()
    assert output_participants == participants


@pytest.mark.parametrize(
    "input_football_teams, output_teams",
    [
        ([FootballTeam(football_api_id=1, name="England")], [Team(football_api_id=1, name="England")]),
        (
            [FootballTeam(football_api_id=1, name="England"), FootballTeam(football_api_id=2, name="France")],
            [Team(football_api_id=1, name="England"), Team(football_api_id=2, name="France")],
        ),
    ],
)
def test_save_and_get_team(
    bot_api: BotApi, input_football_teams: List[FootballTeam], output_teams: List[Team]
) -> None:
    for football_team in input_football_teams:
        bot_api.save_team(football_team)
    teams = bot_api.get_teams()
    assert output_teams == teams


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
