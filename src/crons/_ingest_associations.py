from src.shared.db.api import get_session
from src.shared.bot.api import get_bot_api
from src.shared.db.models import TeamParticipantAssociationORM
DRAW = {
    'Argentina': 'Paddy',
    'Australia': 'Alex',
    'Belgium': 'Sam',
    'Brazil': 'Zoe',
    'Cameroon': 'Zoe',
    'Canada': 'Nathalie',
    'Costa Rica': 'Jack',
    'Croatia': 'Jack',
    'Denmark': 'Delia',
    'Ecuador': 'Moya',
    'England': 'Moya',
    'France': 'Theo',
    'Germany': 'Lucy',
    'Ghana': 'Ludo',
    'Iran': 'Giulia',
    'Japan': 'Hannah',
    'Mexico': 'Ludo',
    'Morocco': 'Paddy',
    'Netherlands': 'Hannah',
    'Poland': 'Ben',
    'Portugal': 'Ben',
    'Qatar': 'Emma',
    'Saudi Arabia': 'Theo',
    'Senegal': 'Lucy',
    'Serbia': 'Sam',
    'South Korea': 'Delia',
    'Spain': 'Nathalie',
    'Switzerland': 'Alex',
    'Tunisia': 'Georgia',
    'USA': 'Giulia',
    'Uruguay': 'Georgia',
    'Wales': 'Emma'
}

if __name__ == "__main__":
    bot_api = get_bot_api()

    participants = bot_api.get_participants()
    teams = bot_api.get_teams()

    participants_mapping = {p.name: p.id for p in participants}
    teams_mapping = {t.name: t.id for t in teams}

    with get_session() as session:
        for team, participant in DRAW.items():
            session.add(
                TeamParticipantAssociationORM(
                    team_id=teams_mapping[team],
                    participant_id=participants_mapping[participant]
                )
            )
        session.commit()
