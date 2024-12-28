# workers/handlers.py
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from magic_filter import F

from tgbot.api.order import APIClient
from tgbot.keyboards.inline import create_pagination_keyboard
from tgbot.utils import ITEMS_PER_PAGE, format_worker_list

workers_router = Router()


@workers_router.message(F.text == "Мастера")
async def get_workers_list(message: Message,state: FSMContext):
    """Handle initial workers list request."""
    await state.clear()
    api_client = APIClient()
    try:
        response = await api_client.get_workers(page=1)
        workers = response.get("results", [])
        total_count = response.get("count", 0)
        total_pages = (total_count + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

        text = format_worker_list(workers)
        text += (
            f"📄 Страница 1 из {total_pages}\n"
            f"📊 Всего специалистов: {total_count}"
        )

        keyboard = create_pagination_keyboard(1, total_pages, "workers")
        await message.reply(text, reply_markup=keyboard, parse_mode="HTML")

    except Exception as e:
        await message.reply(f"❌ Ошибка при получении списка мастеров: {str(e)}")


@workers_router.callback_query(F.data.startswith("workers"))
async def handle_workers_pagination(callback_query: CallbackQuery):
    """Handle workers list pagination."""
    if not callback_query.message:
        await callback_query.answer("Cannot process this request")
        return

    api_client = APIClient()
    try:
        print(callback_query.data)
        action, page = callback_query.data.split(":")[1:]
        page = int(page)

        response = await api_client.get_workers(page=page)
        workers = response.get("results", [])
        total_count = response.get("count", 0)
        total_pages = (total_count + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

        text = format_worker_list(workers)
        text += (
            f"📄 Страница {page} из {total_pages}\n"
            f"📊 Всего специалистов: {total_count}"
        )

        keyboard = create_pagination_keyboard(page, total_pages, "workers")
        await callback_query.message.edit_text(
            text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        await callback_query.answer()

    except Exception as e:
        if callback_query.message:
            await callback_query.message.edit_text(f"❌ Ошибка: {str(e)}")
        await callback_query.answer("Произошла ошибка при обработке запроса")


@workers_router.callback_query(F.data == "current_page")
async def handle_current_page(callback_query: CallbackQuery):
    """Handle current page button press."""
    await callback_query.answer("Текущая страница")
