import time

from src.shared.bot_api.api import get_bot_api
from src.shared.schemas import SweepstakeCategoryIDEnum
from src.shared.telegram_api.api import get_telegram_api


def main() -> None:
    bot_api = get_bot_api()
    telegram_api = get_telegram_api()
    telegram_api.send_message("Yo folks, daily update 👇")
    time.sleep(2)

    sweepstake_category = bot_api.get_sweepstake_category(SweepstakeCategoryIDEnum.WORST_TEAM)
    worst_team, data = bot_api.get_worst_team()
    telegram_api.send_message(
        f'🏆 The winner of "{sweepstake_category.name}" is {worst_team.name} {worst_team.emoji} drawn by '
        f"{worst_team.participant.telegram_tag}, they win £{sweepstake_category.reward_amount} 💸\n"
        f'{worst_team.emoji} {worst_team.name} lost {data["losses"]} matches, scoring {data["goals_scored"]} goal and '
        f'conceding {data["goals_conceded"]} 💀'
    )
    time.sleep(2)

    sweepstake_category = bot_api.get_sweepstake_category(SweepstakeCategoryIDEnum.FILTHIEST_TEAM)
    filthiest_team, data = bot_api.get_filthiest_team()
    telegram_api.send_message(
        f'🏆 The winner (so-far) of "{sweepstake_category.name}" is {filthiest_team.name} {filthiest_team.emoji} '
        f"drawn by {filthiest_team.participant.telegram_tag}, they could win £{sweepstake_category.reward_amount} 💸\n"
        f'{filthiest_team.emoji} {filthiest_team.name} had {data["yellow"]} yellow cards 🟨, {data["yellow_then_red"]} '
        f'yellows converted into reds 🟨🟥 and {data["red"]} red 🟥'
    )
    time.sleep(2)

    sweepstake_category = bot_api.get_sweepstake_category(SweepstakeCategoryIDEnum.EARLIEST_GOAL)
    earliest_goal_team, data = bot_api.get_earliest_goal()
    telegram_api.send_message(
        f'🏆 The winner (so-far) of "{sweepstake_category.name}" is {earliest_goal_team.name} '
        f"{earliest_goal_team.emoji} drawn by {earliest_goal_team.participant.telegram_tag}, they could win "
        f"£{sweepstake_category.reward_amount} 💸\n"
        f'{earliest_goal_team.emoji} {earliest_goal_team.name} scored {data["minutes_elapsed"]} minutes into the first'
        f' half. {data["player_full_name"]} scored against {data["against_team_name"]} on {data["date"]} ⚽'
    )
    time.sleep(2)

    sweepstake_category = bot_api.get_sweepstake_category(SweepstakeCategoryIDEnum.LATEST_GOAL)
    latest_goal_team, data = bot_api.get_latest_goal()
    telegram_api.send_message(
        f'🏆 The winner (so-far) of "{sweepstake_category.name}" is {latest_goal_team.name} {latest_goal_team.emoji} '
        f"drawn by {latest_goal_team.participant.telegram_tag}, they could win £{sweepstake_category.reward_amount} 💸\n"
        f'{latest_goal_team.emoji} {latest_goal_team.name} scored {data["minutes_elapsed"]} minutes after the 90th '
        f'minute. {data["player_full_name"]} scored against {data["against_team_name"]} on {data["date"]} ⚽'
    )
    time.sleep(2)

    sweepstake_category = bot_api.get_sweepstake_category(SweepstakeCategoryIDEnum.YOUNGEST_GOAL_SCORER)
    youngest_goalscorer_team, data = bot_api.get_youngest_goalscorer()
    telegram_api.send_message(
        f'🏆 The winner (so-far) of "{sweepstake_category.name}" is {youngest_goalscorer_team.name} '
        f"{youngest_goalscorer_team.emoji} drawn by {youngest_goalscorer_team.participant.telegram_tag}, they could "
        f"win £{sweepstake_category.reward_amount} 💸\n"
        f"{youngest_goalscorer_team.emoji} {youngest_goalscorer_team.name}'s {data['player_full_name']} scored at "
        f"only {data['age']} 🦵⚽"
    )
    time.sleep(2)

    sweepstake_category = bot_api.get_sweepstake_category(SweepstakeCategoryIDEnum.OLDEST_GOAL_SCORER)
    oldest_goalscorer_team, data = bot_api.get_oldest_goalscorer()
    telegram_api.send_message(
        f'🏆 The winner (so-far) of "{sweepstake_category.name}" is {oldest_goalscorer_team.name} '
        f"{oldest_goalscorer_team.emoji} drawn by {oldest_goalscorer_team.participant.telegram_tag}, they could win "
        f"£{sweepstake_category.reward_amount} 💸\n"
        f"{oldest_goalscorer_team.emoji} {oldest_goalscorer_team.name}'s {data['player_full_name']} scored at the"
        f" whopping age of {data['age']} 🦵⚽"
    )

    telegram_api.send_message("🤔 Who's in and who's out ❓")
    for team in bot_api.get_remaining_teams():
        telegram_api.send_message(f"{team.emoji_and_name} is still in, well done {team.participant.telegram_tag} ✅")
        time.sleep(1)

    for team in bot_api.get_non_remaining_teams():
        telegram_api.send_message(f"{team.emoji_and_name} is still in, suck it {team.participant.telegram_tag} ❌")
        time.sleep(1)


if __name__ == "__main__":
    main()
