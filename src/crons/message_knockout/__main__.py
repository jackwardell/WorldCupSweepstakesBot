import time
from collections import defaultdict

from src.shared.bot_api.api import get_bot_api
from src.shared.telegram_api.api import get_telegram_api


def main() -> None:
    bot_api = get_bot_api()
    telegram_api = get_telegram_api()

    all_team_football_api_ids = {t.football_api_id for t in bot_api.get_teams()}

    all_remaining_football_api_ids = {
        item
        for sublist in [
            [fixture.away_team.football_api_id, fixture.home_team.football_api_id]
            for fixture in bot_api.get_fixtures(today_only=False)
            if fixture.round == "Round of 16"
        ]
        for item in sublist
    }

    loser_teams_football_api_ids = all_team_football_api_ids - all_remaining_football_api_ids

    loser_teams = [bot_api.get_team(team_id) for team_id in loser_teams_football_api_ids]

    telegram_api.send_message("Alright folks, time to announce the losers 👇")

    loser_tag_to_count = defaultdict(int)

    for team in loser_teams:
        telegram_api.send_message(f"❌ {team.name} is out, get rekt {team.participant.telegram_tag} 💀")
        loser_tag_to_count[team.participant.telegram_tag] += 1
        time.sleep(1)

    time.sleep(5)
    telegram_api.send_message("This means we have some serious losers amongst us 👇")

    msg = ", ".join([i for i, j in loser_tag_to_count.items() if j == 2])
    telegram_api.send_message(f"👎 {msg} 👎")


if __name__ == "__main__":
    main()
