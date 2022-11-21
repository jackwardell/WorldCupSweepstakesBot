from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.shared.config import get_config

engine = create_engine(get_config().SQLALCHEMY_URL)


def get_session() -> Session:
    return Session(engine)
