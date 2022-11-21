from __future__ import annotations

from functools import lru_cache
from telegram.utils.types import FileInput
from typing import List
from src.shared.config import PROJECT_ROOT
import attr
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from telegram import Bot, ParseMode

from src.shared.config import get_config
from src.shared.telegram_api.models import TelegramUser

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
        message = self.bot.send_message(
            self.chat_id,
            message,
            reply_to_message_id=reply_to_message_id,
            parse_mode=ParseMode.MARKDOWN,
        )
        return message.message_id

    def send_photo(self, image: FileInput, message: str, reply_to_message_id: int = None) -> int:
        return self.bot.send_photo(self.chat_id, image, message, reply_to_message_id=reply_to_message_id).message_id

    def pin_message(self, message_id: int) -> bool:
        return self.bot.pin_chat_message(self.chat_id, message_id)

    def send_spider_man_image(self, participant_name: str) -> int:
        image_name = f"spiderman-{participant_name}.jpg"
        image_path = PROJECT_ROOT / "assets" / image_name
        if image_path.exists():
            return image_path
        else:
            spiderman_image = Image.open(str(image_path / "assets/spiderman.jpg"))
            draw = ImageDraw.Draw(spiderman_image)
            font = ImageFont.truetype(str(image_path / "assets/OpenSans-Bold.ttf"), 64)
            draw.text((100, 175), participant_name, (0, 0, 0), font=font)
            draw.text((520, 225), participant_name, (0, 0, 0), font=font)
            spiderman_image.save(str(image_path))

        with open(image_path, "rb") as jpg:
            return self.send_photo(jpg, "🤔")

    def get_users(self) -> List[TelegramUser]:
        return [
            TelegramUser.from_telegram(m.user)
            for m in self.bot.get_chat(self.chat_id).get_administrators()
            if m.user.first_name != BOT_NAME
        ]
