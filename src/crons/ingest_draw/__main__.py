from loguru import logger
from src.shared.bot_api.api import BotApiError
from src.shared.bot_api.api import get_bot_api

DRAW = {
    26: 1501950617,
    20: 1625076769,
    1: 5856623337,
    6: 1506652150,
    1530: 1506652150,
    5529: 1774873510,
    29: 768615337,
    3: 768615337,
    21: 1677664317,
    2382: 5132466281,
    10: 5132466281,
    2: 830516211,
    25: 1593812378,
    1504: 5800419423,
    22: 1649097866,
    12: 1554408735,
    16: 5800419423,
    31: 1501950617,
    1118: 1554408735,
    24: 5592358621,
    27: 5592358621,
    1569: 1529068167,
    23: 830516211,
    13: 1593812378,
    14: 5856623337,
    17: 1677664317,
    9: 1774873510,
    15: 1625076769,
    28: 5598841720,
    2384: 1649097866,
    7: 5598841720,
    767: 1529068167,
}


def main() -> None:
    logger.info("running ingest_draw")

    bot_api = get_bot_api()

    for team_id, participant_id in DRAW.items():
        try:
            bot_api.save_team_drawn_by_participant(team_id, participant_id)
        except BotApiError:
            pass


if __name__ == "__main__":
    main()
