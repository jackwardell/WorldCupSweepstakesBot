from __future__ import annotations

from datetime import date
from datetime import datetime

from src.shared.football_api.responses import FootballApiFixtureEventsResponse
from src.shared.football_api.responses import FootballApiFixtureResponse
from src.shared.football_api.responses import FootballApiPlayerResponse
from src.shared.football_api.responses import FootballApiTeamResponse
from src.shared.schemas import FixtureEventSchema
from src.shared.schemas import FixtureSchema
from src.shared.schemas import PlayerSchema
from src.shared.schemas import TeamSchema


class FootballTeam(TeamSchema):
    @classmethod
    def from_football_api_response(cls, response: FootballApiTeamResponse) -> FootballTeam:
        team = cls(
            football_api_id=response["response"]["team"]["id"],
            name=response["response"]["team"]["name"],
        )
        return team


class FootballFixture(FixtureSchema):
    home_team_football_api_id: int
    away_team_football_api_id: int

    @classmethod
    def from_football_api_response(cls, response: FootballApiFixtureResponse) -> FootballFixture:
        fixture = cls(
            football_api_id=response["response"]["fixture"]["id"],
            home_team_football_api_id=response["response"]["teams"]["home"]["id"],
            away_team_football_api_id=response["response"]["teams"]["away"]["id"],
            home_team_goals=response["response"]["goals"]["home"],
            away_team_goals=response["response"]["goals"]["away"],
            home_team_winner=response["response"]["teams"]["home"]["winner"],
            away_team_winner=response["response"]["teams"]["away"]["winner"],
            kick_off=datetime.fromisoformat(response["response"]["fixture"]["date"]),
            venue_city=response["response"]["fixture"]["venue"]["city"],
            venue_name=response["response"]["fixture"]["venue"]["name"],
            round=response["response"]["league"]["round"],
            home_goals_halftime=response["response"]["score"]["halftime"]["home"],
            away_goals_halftime=response["response"]["score"]["halftime"]["away"],
            home_goals_fulltime=response["response"]["score"]["fulltime"]["home"],
            away_goals_fulltime=response["response"]["score"]["fulltime"]["away"],
            away_goals_extratime=response["response"]["score"]["extratime"]["home"],
            home_goals_extratime=response["response"]["score"]["extratime"]["away"],
            home_goals_penalties=response["response"]["score"]["penalty"]["home"],
            away_goals_penalties=response["response"]["score"]["penalty"]["away"],
        )
        return fixture


class FootballPlayer(PlayerSchema):
    @classmethod
    def from_football_api_response(cls, response: FootballApiPlayerResponse) -> FootballPlayer:
        assert len(response["response"]["statistics"]) == 1
        player = cls(
            football_api_id=response["response"]["player"]["id"],
            first_name=response["response"]["player"]["firstname"],
            last_name=response["response"]["player"]["lastname"],
            date_of_birth=date.fromisoformat(response["response"]["player"]["birth"]["date"]),
            team_football_api_id=response["response"]["statistics"][0]["team"]["id"],
            yellow_cards=response["response"]["statistics"][0]["cards"]["yellow"],
            yellow_then_red_cards=response["response"]["statistics"][0]["cards"]["yellowred"],
            red_cards=response["response"]["statistics"][0]["cards"]["red"],
            goals=response["response"]["statistics"][0]["goals"]["total"],
        )
        return player


class FootballFixtureEvent(FixtureEventSchema):
    @classmethod
    def from_football_api_response(cls, response: FootballApiFixtureEventsResponse) -> FootballFixtureEvent:
        fixture_event = cls(
            fixture_football_api_id=response["parameters"]["fixture"],
            time_elapsed_min=response["response"]["time"]["elapsed"],
            time_elapsed_extra_min=response["response"]["time"]["extra"],
            team_football_api_id=response["response"]["team"]["id"],
            player_football_api_id=response["response"]["player"]["id"],
            type=response["response"]["type"],
            detail=response["response"]["detail"],
        )
        return fixture_event
