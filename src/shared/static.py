from __future__ import annotations
from enum import Enum
from pydantic import BaseModel


class Team(BaseModel):
    name: str
    group: str
    seed: int
    emoji: str


class Teams(Enum):
    ARGENTINA = Team(name="Argentina", group="C", seed=4, emoji="🇦🇷")
    AUSTRALIA = Team(name="Australia", group="D", seed=42, emoji="🇦🇺")
    BELGIUM = Team(name="Belgium", group="F", seed=2, emoji="🇧🇪")
    BRAZIL = Team(name="Brazil", group="G", seed=1, emoji="🇧🇷")
    CAMEROON = Team(name="Cameroon", group="G", seed=37, emoji="🇨🇲")
    CANADA = Team(name="Canada", group="F", seed=38, emoji="🇨🇦")
    COSTA_RICA = Team(name="Costa Rica", group="E", seed=31, emoji="🇨🇷")
    CROATIA = Team(name="Croatia", group="F", seed=16, emoji="🇭🇷")
    DENMARK = Team(name="Denmark", group="D", seed=11, emoji="🇩🇰")
    ECUADOR = Team(name="Ecuador", group="A", seed=46, emoji="🇪🇨")
    ENGLAND = Team(name="England", group="B", seed=5, emoji="🏴󠁧󠁢󠁥󠁮󠁧󠁿")
    FRANCE = Team(name="France", group="D", seed=3, emoji="🇫🇷")
    GERMANY = Team(name="Germany", group="E", seed=12, emoji="🇩🇪")
    GHANA = Team(name="Ghana", group="H", seed=60, emoji="🇬🇭")
    IRAN = Team(name="Iran", group="B", seed=21, emoji="🇮🇷")
    JAPAN = Team(name="Japan", group="E", seed=23, emoji="🇯🇵")
    MEXICO = Team(name="Mexico", group="C", seed=9, emoji="🇲🇽")
    MOROCCO = Team(name="Morocco", group="F", seed=24, emoji="🇲🇦")
    NETHERLANDS = Team(name="Netherlands", group="A", seed=10, emoji="🇳🇱")
    POLAND = Team(name="Poland", group="C", seed=26, emoji="🇵🇱")
    PORTUGAL = Team(name="Portugal", group="H", seed=8, emoji="🇵🇹")
    QATAR = Team(name="Qatar", group="A", seed=51, emoji="🇶🇦")
    SAUDI_ARABIA = Team(name="Saudi Arabia", group="C", seed=49, emoji="🇸🇦")
    SENEGAL = Team(name="Senegal", group="A", seed=20, emoji="🇸🇳")
    SERBIA = Team(name="Serbia", group="G", seed=25, emoji="🇷🇸")
    SOUTH_KOREA = Team(name="South Korea", group="H", seed=29, emoji="🇰🇷")
    SPAIN = Team(name="Spain", group="E", seed=7, emoji="🇪🇸")
    SWITZERLAND = Team(name="Switzerland", group="G", seed=14, emoji="🇨🇭")
    TUNISIA = Team(name="Tunisia", group="D", seed=35, emoji="🇹🇳")
    USA = Team(name="USA", group="B", seed=15, emoji="🇺🇸")
    URUGUAY = Team(name="Uruguay", group="H", seed=13, emoji="🇺🇾")
    WALES = Team(name="Wales", group="B", seed=18, emoji="🏴󠁧󠁢󠁷󠁬󠁳󠁿")

    @classmethod
    def get_team(cls, name: str) -> Team:
        return {t.value.name: t for t in cls.__members__.values()}[name].value


class Participants(Enum):
    JACK = "Jack"
    ZOE = "Zoë"
    PADDY = "Paddy"
    LUCY = "Lucy"
    GIULIA = "Giulia"
    EMMA = "Emma"
    DELIA = "Delia"
    HANNAH = "Hannah"
    NAT = "Nat"
    GEORGIA = "Georgia"
    BEN = "Ben"
    ROMANNE = "Romanne"
