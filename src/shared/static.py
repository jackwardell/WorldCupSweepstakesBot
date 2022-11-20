from __future__ import annotations
from enum import Enum
from pydantic import BaseModel
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Participant(BaseModel):
    name: str
    display_name: str
    telegram_id: int


class Team(BaseModel):
    name: str
    group: str
    seed: int
    emoji: str
    participant: Participant




class Teams(Enum):
    ARGENTINA = Team(name="Argentina", group="C", seed=4, emoji="🇦🇷", participant=Participants.PADDY.value)
    AUSTRALIA = Team(name="Australia", group="D", seed=42, emoji="🇦🇺", participant=Participants.ALEX.value)
    BELGIUM = Team(name="Belgium", group="F", seed=2, emoji="🇧🇪", participant=Participants.SAM.value)
    BRAZIL = Team(name="Brazil", group="G", seed=1, emoji="🇧🇷", participant=Participants.ZOE.value)
    CAMEROON = Team(name="Cameroon", group="G", seed=37, emoji="🇨🇲", participant=Participants.ZOE.value)
    CANADA = Team(name="Canada", group="F", seed=38, emoji="🇨🇦", participant=Participants.NATHALIE.value)
    COSTA_RICA = Team(name="Costa Rica", group="E", seed=31, emoji="🇨🇷", participant=Participants.JACK.value)
    CROATIA = Team(name="Croatia", group="F", seed=16, emoji="🇭🇷", participant=Participants.JACK.value)
    DENMARK = Team(name="Denmark", group="D", seed=11, emoji="🇩🇰", participant=Participants.DELIA.value)
    ECUADOR = Team(name="Ecuador", group="A", seed=46, emoji="🇪🇨", participant=Participants.MOYA.value)
    ENGLAND = Team(name="England", group="B", seed=5, emoji="🏴󠁧󠁢󠁥󠁮󠁧󠁿", participant=Participants.MOYA.value)
    FRANCE = Team(name="France", group="D", seed=3, emoji="🇫🇷", participant=Participants.THEO.value)
    GERMANY = Team(name="Germany", group="E", seed=12, emoji="🇩🇪", participant=Participants.LUCY.value)
    GHANA = Team(name="Ghana", group="H", seed=60, emoji="🇬🇭", participant=Participants.LUDO.value)
    IRAN = Team(name="Iran", group="B", seed=21, emoji="🇮🇷", participant=Participants.GIULIA.value)
    JAPAN = Team(name="Japan", group="E", seed=23, emoji="🇯🇵", participant=Participants.HANNAH.value)
    MEXICO = Team(name="Mexico", group="C", seed=9, emoji="🇲🇽", participant=Participants.LUDO.value)
    MOROCCO = Team(name="Morocco", group="F", seed=24, emoji="🇲🇦", participant=Participants.PADDY.value)
    NETHERLANDS = Team(name="Netherlands", group="A", seed=10, emoji="🇳🇱", participant=Participants.HANNAH.value)
    POLAND = Team(name="Poland", group="C", seed=26, emoji="🇵🇱", participant=Participants.BEN.value)
    PORTUGAL = Team(name="Portugal", group="H", seed=8, emoji="🇵🇹", participant=Participants.BEN.value)
    QATAR = Team(name="Qatar", group="A", seed=51, emoji="🇶🇦", participant=Participants.EMMA.value)
    SAUDI_ARABIA = Team(name="Saudi Arabia", group="C", seed=49, emoji="🇸🇦", participant=Participants.THEO.value)
    SENEGAL = Team(name="Senegal", group="A", seed=20, emoji="🇸🇳", participant=Participants.LUCY.value)
    SERBIA = Team(name="Serbia", group="G", seed=25, emoji="🇷🇸", participant=Participants.SAM.value)
    SOUTH_KOREA = Team(name="South Korea", group="H", seed=29, emoji="🇰🇷", participant=Participants.DELIA.value)
    SPAIN = Team(name="Spain", group="E", seed=7, emoji="🇪🇸", participant=Participants.NATHALIE.value)
    SWITZERLAND = Team(name="Switzerland", group="G", seed=14, emoji="🇨🇭", participant=Participants.ALEX.value)
    TUNISIA = Team(name="Tunisia", group="D", seed=35, emoji="🇹🇳", participant=Participants.GEORGIA.value)
    USA = Team(name="USA", group="B", seed=15, emoji="🇺🇸", participant=Participants.GIULIA.value)
    URUGUAY = Team(name="Uruguay", group="H", seed=13, emoji="🇺🇾", participant=Participants.GEORGIA.value)
    WALES = Team(name="Wales", group="B", seed=18, emoji="🏴󠁧󠁢󠁷󠁬󠁳󠁿", participant=Participants.EMMA.value)

    @classmethod
    def get_team(cls, name: str) -> Team:
        return {t.value.name: t for t in cls.__members__.values()}[name].value
