from __future__ import annotations

from functools import lru_cache

import attr
from telegram import Bot, Chat, User
from typing import List
from src.shared.config import get_config
from pydantic import BaseModel


@lru_cache
def get_telegram_bot() -> TelegramBot:
    return TelegramBot()


class TelegramUser(BaseModel):
    id: int
    first_name: str
    last_name: str

    @classmethod
    def from_telegram(cls, user: User):
        return cls(id=user.id, first_name=user.first_name, last_name=user.last_name)


@attr.s
class TelegramBot:
    bot: Bot = attr.ib(factory=lambda: Bot(get_config().TELEGRAM_API_KEY))
    chat_id: str = attr.ib(factory=lambda: get_config().TELEGRAM_CHAT_ID)

    def send_message(self, message: str) -> None:
        self.bot.send_message(self.chat_id, message)

    def _get_chat(self) -> Chat:
        return self.bot.get_chat(self.chat_id)

    def get_users(self) -> List[TelegramUser]:
        members = self._get_chat().get_administrators()
        return [TelegramUser.from_telegram(member.user) for member in members]
