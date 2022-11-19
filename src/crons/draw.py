import random

from src.shared.static import Participants
from src.shared.static import Teams

if __name__ == "__main__":
    all_teams = sorted([t.value for t in Teams.__members__.values()], key=lambda x: x.seed)
    tier_one_teams = all_teams[: len(all_teams) // 2]
    tier_two_teams = all_teams[len(all_teams) // 2 :]

    random.shuffle(tier_one_teams)
    random.shuffle(tier_two_teams)

    for participant in Participants.__members__.values():
        draw_one = tier_one_teams.pop()
        message = f"🎉 {participant.value} has got {draw_one.name} {draw_one.emoji} for their tier one team 🎉"
        print(message)

    for participant in Participants.__members__.values():
        draw_two = tier_two_teams.pop()
        message = f"🎉 {participant.value} has got {draw_two.name} {draw_two.emoji} for their tier two team 🎉"
        print(message)
