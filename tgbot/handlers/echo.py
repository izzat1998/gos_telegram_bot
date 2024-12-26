from aiogram import types, Router, F
from aiogram.filters import StateFilter

echo_router = Router()

#
# @echo_router.message(F.text, StateFilter(None))
# async def bot_echo(message: types.Message):
#     text = message.text
#
#     await message.answer("\n".join(text))
