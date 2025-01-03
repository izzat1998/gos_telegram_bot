from aiogram.filters import BaseFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message

from tgbot.config import Config


class AdminFilter(BaseFilter):
    is_admin: bool = True

    async def __call__(self, obj: Message, config: Config) -> bool:
        if obj.from_user is None:
            return False
        return (obj.from_user.id in config.tg_bot.admin_ids) == self.is_admin

