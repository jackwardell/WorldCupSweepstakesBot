from __future__ import annotations

from functools import lru_cache

import attr
from telegram import Bot

from src.shared.config import get_config


@lru_cache
def get_telegram_bot() -> TelegramBot:
    return TelegramBot()


@attr.s
class TelegramBot:
    bot: Bot = attr.ib(factory=lambda: Bot(get_config().TELEGRAM_API_KEY))
    chat_id: str = attr.ib(factory=lambda: get_config().TELEGRAM_CHAT_ID)

    def send_message(self, message: str) -> None:
        self.bot.send_message(self.chat_id, message)
