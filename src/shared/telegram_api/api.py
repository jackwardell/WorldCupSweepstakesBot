from __future__ import annotations

from functools import lru_cache
from typing import List

import attr
from src.shared.config import get_config
from src.shared.config import PROJECT_ROOT
from src.shared.telegram_api.models import TelegramUser
from telegram import Bot
from telegram.utils.types import FileInput

# from telegram import ParseMode

BOT_NAME = "WorldCupBot2022"


@lru_cache
def get_telegram_api() -> TelegramApi:
    return TelegramApi()


@attr.s
class TelegramApi:
    bot: Bot = attr.ib(factory=lambda: Bot(get_config().TELEGRAM_API_KEY))
    chat_id: str = attr.ib(factory=lambda: get_config().TELEGRAM_CHAT_ID)

    def send_message(self, message: str, reply_to_message_id: int = None) -> int:
        print(message)
        # message = self.bot.send_message(
        #     self.chat_id,
        #     message,
        #     reply_to_message_id=reply_to_message_id,
        #     parse_mode=ParseMode.MARKDOWN,
        # )
        # return message.message_id

    def send_photo(self, image: FileInput, message: str, reply_to_message_id: int = None) -> int:
        return self.bot.send_photo(self.chat_id, image, message, reply_to_message_id=reply_to_message_id).message_id

    def pin_message(self, message_id: int) -> bool:
        return self.bot.pin_chat_message(self.chat_id, message_id)

    def send_spiderman_image(self, participant_name: str, reply_to_message_id: int = None) -> int:
        image_path = PROJECT_ROOT / "src" / "assets" / "rendered_assets" / f"spiderman-{participant_name}.jpg"
        with open(image_path, "rb") as jpg:
            return self.send_photo(jpg, "🤔", reply_to_message_id=reply_to_message_id)

    def get_users(self) -> List[TelegramUser]:
        administrators = self.bot.get_chat(self.chat_id).get_administrators()
        return [TelegramUser.from_telegram(a.user) for a in administrators if a.user.first_name != BOT_NAME]
