from src.shared.bot.api import get_bot_api
from src.shared.db.api import get_session
from src.shared.db.models import ParticipantORM

if __name__ == "__main__":
    bot_api = get_bot_api()

    fixtures = get_bot_api().get_fixtures()

    print(fixtures)
    #
    # with get_session() as session:
    #     for user in users:
    #         participant = ParticipantORM.from_telegram_user(user)
    #         session.add(participant)
    #
    #     session.commit()
