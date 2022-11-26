from __future__ import annotations

from src.shared.schemas import ParticipantSchema
from telegram import User


class TelegramParticipant(ParticipantSchema):
    @classmethod
    def from_telegram(cls, user: User) -> TelegramParticipant:
        return cls(id=user.id, first_name=user.first_name)
