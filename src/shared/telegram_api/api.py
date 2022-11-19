from __future__ import annotations

from functools import lru_cache
from typing import List

import attr
from telegram import Bot

from src.shared.config import get_config
from src.shared.telegram_api.models import TelegramUser


@lru_cache
def get_telegram_api() -> TelegramApi:
    return TelegramApi()


@attr.s
class TelegramApi:
    bot: Bot = attr.ib(factory=lambda: Bot(get_config().TELEGRAM_API_KEY))
    chat_id: str = attr.ib(factory=lambda: get_config().TELEGRAM_CHAT_ID)

    def send_message(self, message: str) -> None:
        return self.bot.send_message(self.chat_id, message)

    def get_users(self) -> List[TelegramUser]:
        return [TelegramUser.from_telegram(m.user) for m in self.bot.get_chat(self.chat_id).get_administrators()]
