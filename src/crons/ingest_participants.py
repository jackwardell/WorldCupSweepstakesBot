from src.shared.telegram_api.api import get_telegram_api
from src.shared.db.api import get_session
from src.shared.db.models import Participant

if __name__ == "__main__":
    telegram_api = get_telegram_api()

    users = get_telegram_api().get_users()

    with get_session() as session:
        for user in users:
            participant = Participant.from_telegram_user(user)
            session.add(participant)

        session.commit()
