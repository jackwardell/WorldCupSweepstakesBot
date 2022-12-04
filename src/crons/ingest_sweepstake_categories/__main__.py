from loguru import logger
from src.shared.bot_api.api import BotApi
from src.shared.schemas import SweepstakeCategoryEnum

CATEGORIES = [
    {"id": SweepstakeCategoryEnum.WINNING_TEAM, "name": "Winning Team", "reward_amount": 50},
    {"id": SweepstakeCategoryEnum.WORST_TEAM, "name": "Worst Team", "reward_amount": 20},
    {"id": SweepstakeCategoryEnum.MOST_MEANINGFUL_PROTEST, "name": "Most Meaningful Protest", "reward_amount": 20},
    {"id": SweepstakeCategoryEnum.FILTHIEST_TEAM, "name": "Filthiest Team", "reward_amount": 20},
    {"id": SweepstakeCategoryEnum.EARLIEST_GOAL, "name": "Earliest Goal", "reward_amount": 15},
    {"id": SweepstakeCategoryEnum.LATEST_GOAL, "name": "Latest Goal", "reward_amount": 15},
    {"id": SweepstakeCategoryEnum.OLDEST_GOAL_SCORER, "name": "Oldest Goal Scorer", "reward_amount": 10},
    {"id": SweepstakeCategoryEnum.YOUNGEST_GOAL_SCORER, "name": "Youngest Goal Scorer", "reward_amount": 10},
]


def main() -> None:
    logger.info("running ingest_sweepstake_categories")

    bot_api = BotApi()
    for category in CATEGORIES:
        bot_api.save_sweepstake_category(
            sweepstake_category_enum=category["id"],
            sweepstake_category_name=category["name"],
            sweepstake_category_reward_amount=category["reward_amount"],
        )


if __name__ == "__main__":
    main()
