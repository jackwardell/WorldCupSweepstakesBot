import random

from src.shared.static import Participants
from src.shared.static import Teams
import time
from src.shared.telegram_api.api import get_telegram_api

# todo remember tg rate limiting
if __name__ == "__main__":
    telegram_api = get_telegram_api()

    telegram_api.send_message("Welcome to the 2022 World Cup Sweepstake 🧹💸")

    message_id = telegram_api.send_message(
        "The rules:\n"
        "1. £10 buy-in for 2 teams\n"
        "2. A donation to a charity of your choice, think about donations to charities supporting migrants or ones in "
        "the countries you draw\n"
        "3. £50 to the winning team, £20 for the worst team, £20 for the team with the most meaningful protest "
        "(chosen by us), £20 for the filthiest team (2 points for red, 1 for yellow), £15 for the earliest goal and "
        "£15 for latest goal that prevents ET or penalties, £10 for the team with the youngest goal scorer and £10 for "
        "the team with the oldest goal scorer.\n"
        "4. The draw will happen alphabetically by first name."
    )
    telegram_api.pin_message(message_id)

    tags = " ".join(
        [f"[{p.value.display_name}](tg://user?id={p.value.telegram_id})" for p in Participants.__members__.values()]
    )

    telegram_api.send_message(f"{tags} The draw will begin in 1 minute.")

    time.sleep(60)

    print("Ok, let the draw begin...")
    time.sleep(5)

    all_teams = sorted([t.value for t in Teams.__members__.values()], key=lambda x: x.seed)
    tier_one_teams = all_teams[: len(all_teams) // 2]
    tier_two_teams = all_teams[len(all_teams) // 2 :]

    random.shuffle(tier_one_teams)
    random.shuffle(tier_two_teams)

    for participant in Participants.__members__.values():
        draw_one = tier_one_teams.pop()
        message = (
            f"🎉 [{participant.value.display_name}](tg://user?id={participant.value.telegram_id}) has got "
            f"{draw_one.name} {draw_one.emoji} for their tier one team 🎉"
        )
        telegram_api.send_message(message)
        time.sleep(2)

    for participant in Participants.__members__.values():
        draw_two = tier_two_teams.pop()
        message = (
            f"🎉 [{participant.value.display_name}](tg://user?id={participant.value.telegram_id}) has got "
            f"{draw_two.name} {draw_two.emoji} for their tier two team 🎉"
        )
        telegram_api.send_message(message)
        time.sleep(2)

    telegram_api.send_message("🍀 Good luck everyone! 🍀")
