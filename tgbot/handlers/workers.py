from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.api.order import APIClient
from tgbot.keyboards.inline import (
    create_pagination_keyboard,
    create_specialization_inline_keyboard,
    SPECIALIZATION_PREFIX, 
    PAGINATION_PREFIX,
    ACTION_ALL,
)

from tgbot.utils import ITEMS_PER_PAGE, format_worker_list
from tgbot.misc.states import Workers

workers_router = Router()

async def handle_api_error(message_or_callback, error: Exception) -> None:
    """Handle API errors consistently across handlers."""
    error_msg = f"❌ Произошла ошибка: {str(error)}"
    
    if isinstance(message_or_callback, CallbackQuery):
        await message_or_callback.answer(error_msg, show_alert=True)
    else:
        await message_or_callback.reply(error_msg)

@workers_router.message(F.text == "👨‍🔧 Мастера")
async def get_specializations(message: Message, state: FSMContext):
    """Handle initial request for specializations list."""
    await state.clear()
    await state.set_state(Workers.specialization)
    
    try:
        api_client = APIClient()
        response = await api_client.get_specializations()
        specializations = response.get("results", [])
        
        if not specializations:
            await message.reply("❌ Список специализаций пуст")
            return
        
        # Store specializations in state
        specializations_map = {spec['name']: spec['slug'] for spec in specializations}
        await state.update_data(specializations_map=specializations_map)

        keyboard = create_specialization_inline_keyboard(specializations)
        await message.reply("👨‍🔧 Выберите специализацию:", reply_markup=keyboard)
        
    except Exception as e:
        await handle_api_error(message, e)

@workers_router.callback_query(F.data.startswith(f"{SPECIALIZATION_PREFIX}:"))
async def handle_specialization_selection(callback: CallbackQuery, state: FSMContext):
    """Handle specialization selection from inline keyboard."""
    action = callback.data.split(":")[1]
    try:
        api_client = APIClient()
        
        if action == ACTION_ALL:
            response = await api_client.get_workers(page=1)
            header = "👥 Все Мастера\n\n"
            await state.update_data(specialization=ACTION_ALL)
        else:
            response = await api_client.get_workers_by_specialization(action, page=1)
            state_data = await state.get_data()
            specializations_map = state_data.get('specializations_map', {})
            specialization_name = next(
                (name for name, slug in specializations_map.items() if slug == action),
                "Неизвестная специализация"
            )
            header = f"👨‍🔧 Мастера - {specialization_name}\n\n"
            await state.update_data(specialization=specialization_name)

        workers = response.get("results", [])
        if not workers:
            await callback.answer("⚠️ Мастера не найдены", show_alert=True)
            return

        total_count = response.get("count", 0)
        total_pages = (total_count + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

        text = header + format_worker_list(workers)
        text += (
            f"\n📄 Страница 1 из {total_pages}\n"
            f"📊 Всего специалистов: {total_count}"
        )

        keyboard = create_pagination_keyboard(1, total_pages, PAGINATION_PREFIX)
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
        await callback.answer()

    except Exception as e:
        await handle_api_error(callback, e)

@workers_router.callback_query(F.data.startswith(f"{PAGINATION_PREFIX}:"))
async def handle_workers_pagination(callback: CallbackQuery, state: FSMContext):
    """Handle workers list pagination."""
    try:
        page = int(callback.data.split(":")[2])
        state_data = await state.get_data()
        specialization = state_data.get('specialization')
        
        api_client = APIClient()
        
        if specialization == ACTION_ALL:
            response = await api_client.get_workers(page=page)
            header = "👥 Все Мастера\n\n"
        else:
            specializations_map = state_data.get('specializations_map', {})
            specialization_slug = next(
                (slug for name, slug in specializations_map.items() if name == specialization),
                None
            )
            if not specialization_slug:
                await callback.answer("❌ Ошибка: специализация не найдена", show_alert=True)
                return
                
            response = await api_client.get_workers_by_specialization(specialization_slug, page=page)
            header = f"👨‍🔧 Мастера - {specialization}\n\n"

        workers = response.get("results", [])
        total_count = response.get("count", 0)
        total_pages = (total_count + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

        text = header + format_worker_list(workers)
        text += (
            f"\n📄 Страница {page} из {total_pages}\n"
            f"📊 Всего специалистов: {total_count}"
        )

        keyboard = create_pagination_keyboard(page, total_pages, PAGINATION_PREFIX)
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
        await callback.answer()

    except Exception as e:
        await handle_api_error(callback, e)
