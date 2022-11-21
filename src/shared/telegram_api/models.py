from __future__ import annotations

from pydantic import BaseModel
from telegram import User


class TelegramUser(BaseModel):
    id: int
    first_name: str

    @classmethod
    def from_telegram(cls, user: User) -> TelegramUser:
        return cls(id=user.id, first_name=user.first_name)
