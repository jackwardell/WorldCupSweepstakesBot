from src.shared.db_api.api import DbApiError
from src.shared.db_api.api import get_db_api

DRAW = {
    "Argentina": "Paddy",
    "Australia": "Alex",
    "Belgium": "Sam",
    "Brazil": "Zoe",
    "Cameroon": "Zoe",
    "Canada": "Nathalie",
    "Costa Rica": "Jack",
    "Croatia": "Jack",
    "Denmark": "Delia",
    "Ecuador": "Moya",
    "England": "Moya",
    "France": "Theo",
    "Germany": "Lucy",
    "Ghana": "Ludo",
    "Iran": "Giulia",
    "Japan": "Hannah",
    "Mexico": "Ludo",
    "Morocco": "Paddy",
    "Netherlands": "Hannah",
    "Poland": "Benjamin",
    "Portugal": "Benjamin",
    "Qatar": "Emma",
    "Saudi Arabia": "Theo",
    "Senegal": "Lucy",
    "Serbia": "Sam",
    "South Korea": "Delia",
    "Spain": "Nathalie",
    "Switzerland": "Alex",
    "Tunisia": "Georgia",
    "USA": "Giulia",
    "Uruguay": "Georgia",
    "Wales": "Emma",
}


def main() -> None:
    db_api = get_db_api()

    for team_name, participant_name in DRAW.items():
        try:
            db_api.save_team_and_participant(team_name, participant_name)
        except DbApiError:
            pass


if __name__ == "__main__":
    main()
