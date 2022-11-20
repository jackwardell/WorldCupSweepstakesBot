from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Participant(Base):
    __tablename__ = "participant"

    name = Column(String, primary_key=True)
    display_name = Column(String)
    telegram_id = Column(Integer)

    @classmethod
    def from_telegram_user(cls) -> Participant:


class Team(Base):
    __tablename__ = "team"

    name = Column(String, primary_key=True)
    emoji = Column(String)


# class ParticipantTeamAssociation(Base):
#     __tablename__ = "participant_team_association"
#
#     team_name =
