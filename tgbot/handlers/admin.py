import locale
from datetime import datetime
from typing import Optional

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from magic_filter import F

from tgbot.api.order import APIClient
from tgbot.filters.admin import AdminFilter
from tgbot.misc.states import OrderStatistics
from tgbot.utils import ORDER_STATUS

admin_router = Router()
admin_router.message.filter(AdminFilter())

locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")
@admin_router.message(CommandStart())
async def admin_start(message: Message):
    buttons = [
        [KeyboardButton(text="📋 Заказы"),KeyboardButton(text="👨‍🔧 Мастера")],
        [KeyboardButton(text="Доставщики"),],
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons, resize_keyboard=True, one_time_keyboard=False
    )

    await message.reply("Здравствуйте, админ!", reply_markup=keyboard)
