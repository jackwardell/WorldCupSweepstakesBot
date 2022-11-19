from __future__ import annotations

from pydantic import BaseModel
from telegram import User


class TelegramUser(BaseModel):
    id: int
    first_name: str
    last_name: str

    @classmethod
    def from_telegram(cls, user: User):
        return cls(id=user.id, first_name=user.first_name, last_name=user.last_name)