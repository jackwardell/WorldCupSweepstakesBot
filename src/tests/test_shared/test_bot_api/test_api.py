# import datetime
from typing import List
from unittest.mock import MagicMock

import pytest
from src.shared.bot_api.api import BotApi
from src.shared.bot_api.db import DrawMappingORM
from src.shared.bot_api.models import Participant
from src.shared.bot_api.models import Team
from src.shared.football_api.models import FootballTeam
from src.shared.telegram_api.models import TelegramParticipant


# from src.shared.bot_api.models import Fixture
# from src.shared.football_api.models import FootballFixture


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


def test_save_draw_mappings(bot_api: BotApi) -> None:
    football_team = FootballTeam(football_api_id=1, name="England")
    telegram_participant = TelegramParticipant(telegram_user_id=69, first_name="Rick")
    bot_api.save_team(football_team)
    bot_api.save_participant(telegram_participant)
    bot_api.save_team_drawn_by_participant(football_team.football_api_id, telegram_participant.telegram_user_id)
    with bot_api.session as session:
        res = session.query(DrawMappingORM).one()
        assert res.team_football_api_id == football_team.football_api_id
        assert res.participant_telegram_user_id == telegram_participant.telegram_user_id

    assert bot_api.get_teams() == [
        Team(football_api_id=1, name="England", participant=Participant(telegram_user_id=69, first_name="Rick"))
    ]


# @pytest.mark.parametrize(
#     "input_football_fixture, output_fixtures",
#     [
#         (
#             [
#                 FootballFixture(
#                     football_api_id=855747,
#                     home_team_football_api_id=1569,
#                     away_team_football_api_id=13,
#                     home_team_goals=1,
#                     away_team_goals=3,
#                     home_team_winner=False,
#                     away_team_winner=True,
#                     kick_off=datetime.datetime(2022, 11, 25, 13, 0, tzinfo=datetime.timezone.utc),
#                     venue_city="Al-Thumama",
#                     venue_name="Al-Thumama Stadium",
#                     round="Group Stage - 2",
#                     home_goals_halftime=0,
#                     away_goals_halftime=1,
#                     home_goals_fulltime=1,
#                     away_goals_fulltime=3,
#                     away_goals_extratime=None,
#                     home_goals_extratime=None,
#                     home_goals_penalties=None,
#                     away_goals_penalties=None,
#                 )
#             ],
#             [
#                 Fixture(
#                     football_api_id=855747,
#                     home_team_football_api_id=1569,
#                     away_team_football_api_id=13,
#                     home_team_goals=1,
#                     away_team_goals=3,
#                     home_team_winner=False,
#                     away_team_winner=True,
#                     kick_off=datetime.datetime(2022, 11, 25, 13, 0, tzinfo=datetime.timezone.utc),
#                     venue_city="Al-Thumama",
#                     venue_name="Al-Thumama Stadium",
#                     round="Group Stage - 2",
#                     home_goals_halftime=0,
#                     away_goals_halftime=1,
#                     home_goals_fulltime=1,
#                     away_goals_fulltime=3,
#                     away_goals_extratime=None,
#                     home_goals_extratime=None,
#                     home_goals_penalties=None,
#                     away_goals_penalties=None,
#                 ),
#             ],
#         ),
#         (
#             [
#                 FootballFixture(
#                     football_api_id=866682,
#                     home_team_football_api_id=767,
#                     away_team_football_api_id=22,
#                     home_team_goals=0,
#                     away_team_goals=2,
#                     home_team_winner=False,
#                     away_team_winner=True,
#                     kick_off=datetime.datetime(2022, 11, 25, 10, 0, tzinfo=datetime.timezone.utc),
#                     venue_city="Al Rayyan",
#                     venue_name="Ahmed bin Ali Stadium",
#                     round="Group Stage - 2",
#                     home_goals_halftime=0,
#                     away_goals_halftime=0,
#                     home_goals_fulltime=0,
#                     away_goals_fulltime=2,
#                     away_goals_extratime=None,
#                     home_goals_extratime=None,
#                     home_goals_penalties=None,
#                     away_goals_penalties=None,
#                 ),
#                 FootballFixture(
#                     football_api_id=855747,
#                     home_team_football_api_id=1569,
#                     away_team_football_api_id=13,
#                     home_team_goals=1,
#                     away_team_goals=3,
#                     home_team_winner=False,
#                     away_team_winner=True,
#                     kick_off=datetime.datetime(2022, 11, 25, 13, 0, tzinfo=datetime.timezone.utc),
#                     venue_city="Al-Thumama",
#                     venue_name="Al-Thumama Stadium",
#                     round="Group Stage - 2",
#                     home_goals_halftime=0,
#                     away_goals_halftime=1,
#                     home_goals_fulltime=1,
#                     away_goals_fulltime=3,
#                     away_goals_extratime=None,
#                     home_goals_extratime=None,
#                     home_goals_penalties=None,
#                     away_goals_penalties=None,
#                 ),
#             ],
#             [
#                 Fixture(
#                     football_api_id=866682,
#                     home_team_football_api_id=767,
#                     away_team_football_api_id=22,
#                     home_team_goals=0,
#                     away_team_goals=2,
#                     home_team_winner=False,
#                     away_team_winner=True,
#                     kick_off=datetime.datetime(2022, 11, 25, 10, 0, tzinfo=datetime.timezone.utc),
#                     venue_city="Al Rayyan",
#                     venue_name="Ahmed bin Ali Stadium",
#                     round="Group Stage - 2",
#                     home_goals_halftime=0,
#                     away_goals_halftime=0,
#                     home_goals_fulltime=0,
#                     away_goals_fulltime=2,
#                     away_goals_extratime=None,
#                     home_goals_extratime=None,
#                     home_goals_penalties=None,
#                     away_goals_penalties=None,
#                 ),
#                 Fixture(
#                     football_api_id=855747,
#                     home_team_football_api_id=1569,
#                     away_team_football_api_id=13,
#                     home_team_goals=1,
#                     away_team_goals=3,
#                     home_team_winner=False,
#                     away_team_winner=True,
#                     kick_off=datetime.datetime(2022, 11, 25, 13, 0, tzinfo=datetime.timezone.utc),
#                     venue_city="Al-Thumama",
#                     venue_name="Al-Thumama Stadium",
#                     round="Group Stage - 2",
#                     home_goals_halftime=0,
#                     away_goals_halftime=1,
#                     home_goals_fulltime=1,
#                     away_goals_fulltime=3,
#                     away_goals_extratime=None,
#                     home_goals_extratime=None,
#                     home_goals_penalties=None,
#                     away_goals_penalties=None,
#                 ),
#             ],
#         ),
#     ],
# )
# def test_save_or_update_and_get_fixtures(
#     bot_api: BotApi, input_football_fixtures: List[FootballFixture], output_fixtures: List[Fixture]
# ) -> None:
#     bot_api.save_or_update_fixture()
