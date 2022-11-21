from src.shared.db.api import get_session
from src.shared.bot.api import get_bot_api
from src.shared.db.models import TeamAndParticipantORM

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

if __name__ == "__main__":
    bot_api = get_bot_api()

    participants = bot_api.get_participants()
    teams = bot_api.get_teams()

    with get_session() as session:
        for team, participant in DRAW.items():
            session.add(
                TeamAndParticipantORM(
                    team_name=team,
                    participant_name=participant,
                )
            )
        session.commit()
