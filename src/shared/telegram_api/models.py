from __future__ import annotations

from src.shared.schemas import UserSchema
from telegram import User


class TelegramUser(UserSchema):
    @classmethod
    def from_telegram(cls, user: User) -> TelegramUser:
        return cls(id=user.id, first_name=user.first_name)
