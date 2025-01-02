from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from tgbot.filters.admin import AdminFilter

import locale
locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")
admin_router = Router()
admin_router.message.filter(AdminFilter())
@admin_router.message(CommandStart())
async def admin_start(message: Message):
    buttons = [
        [
            KeyboardButton(text="📋 Заказы"),
            KeyboardButton(text="👨‍🔧 Мастера"),
        ],
        [KeyboardButton(text="🚚 Доставщики")],
        [KeyboardButton(text="📊 Статистика")]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=False
    )
    

    await message.reply("Добро пожаловать, администратор! Выберите нужный раздел:", reply_markup=keyboard)
