from sqlalchemy import create_engine
from src.shared.config import get_config
from sqlalchemy.orm import Session

engine = create_engine(get_config().SQLALCHEMY_URL)


def get_session() -> Session:
    return Session(engine)
