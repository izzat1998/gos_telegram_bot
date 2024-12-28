from typing import Optional

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from magic_filter import F

from tgbot.api.order import APIClient
from tgbot.keyboards.inline import create_statistics_keyboard, create_orders_list_keyboard
from tgbot.misc.states import OrderStatistics
from tgbot.utils import format_order_detail, ITEMS_PER_PAGE, ORDER_STATUS

orders_router = Router()


@orders_router.message(F.text == "📊 Статистика заказов")
async def get_order_statistics(message: Message, state: FSMContext):
    """Handle order statistics request."""
    api_client = APIClient()
    try:
        statistics = await api_client.get_order_statistics()
        status_dist = statistics["status_distribution"]
        finance = statistics["finance_stats"]
        status_counts = {item["status"]: item["count"] for item in status_dist}

        response = (
            "📈 <b>Финансовая статистика</b>\n"
            f"💰 Общая выручка: {finance['total_revenue']}$\n"
            f"📦 Всего заказов: {finance['total_orders']}\n"
            f"💎 Средний чек: {finance['avg_order_value']}$\n\n"
        )

        keyboard = create_statistics_keyboard(status_counts)
        await state.set_state(OrderStatistics.list_by_status)
        await message.reply(response, parse_mode="HTML", reply_markup=keyboard)

    except Exception as e:
        await message.reply(f"❌ Ошибка при получении статистики: {str(e)}")


# orders/handlers.py (continued)

@orders_router.callback_query(F.data == "back_to_stats")
async def back_to_statistics(callback_query: CallbackQuery, state: FSMContext):
    """Handle back to statistics button."""
    if not callback_query.message:
        await callback_query.answer("Cannot process this request")
        return

    api_client = APIClient()
    try:
        statistics = await api_client.get_order_statistics()
        status_dist = statistics["status_distribution"]
        finance = statistics["finance_stats"]
        status_counts = {item["status"]: item["count"] for item in status_dist}

        response = (
            "📈 <b>Финансовая статистика</b>\n"
            f"💰 Общая выручка: {finance['total_revenue']}$\n"
            f"📦 Всего заказов: {finance['total_orders']}\n"
            f"💎 Средний чек: {finance['avg_order_value']}$\n\n"
        )

        keyboard = create_statistics_keyboard(status_counts)
        await state.set_state(OrderStatistics.list_by_status)
        await callback_query.message.edit_text(
            response,
            parse_mode="HTML",
            reply_markup=keyboard
        )
        await callback_query.answer()

    except Exception as e:
        await callback_query.message.edit_text(f"❌ Ошибка: {str(e)}")
        await callback_query.answer()


@orders_router.callback_query(F.data.startswith("order:"))
async def get_order_detail(callback_query: CallbackQuery):
    """Handle order detail request."""
    if not callback_query.message:
        await callback_query.answer("Cannot process this request")
        return

    try:
        order_id = callback_query.data.split(":")[1]
        api_client = APIClient()
        order = await api_client.get_order_detail(order_id)

        # Get current page from message text for back button
        current_page = get_current_page_from_message(callback_query.message.text)

        # Format order details
        response = format_order_detail(order)

        # Create back button
        back_button = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text="🔙 Назад к списку",
                    callback_data=f"{order['status']}:next:{current_page}"
                )
            ]]
        )

        await callback_query.message.edit_text(
            response,
            parse_mode="HTML",
            reply_markup=back_button
        )
        await callback_query.answer()

    except Exception as e:
        await callback_query.message.edit_text(f"❌ Ошибка: {str(e)}")
        await callback_query.answer()


@orders_router.callback_query(OrderStatistics.list_by_status)
async def get_order_list_by_status(callback_query: CallbackQuery,state: FSMContext):
    """Handle order list by status request."""
    if not callback_query.message:
        await callback_query.answer("Cannot process this request")
        return

    api_client = APIClient()
    data_parts = callback_query.data.split(":")

    try:
        # Parse status and page
        if len(data_parts) == 1:
            order_status = data_parts[0]
            current_page = 1
        else:
            order_status, _, page = data_parts
            current_page = int(page)

        # Get orders for the current page
        response = await api_client.get_order_list_by_status(
            order_status,
            page=current_page
        )

        orders = response.get("results", [])
        total_count = response.get("count", 0)
        total_pages = (total_count + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

        # Create keyboard with orders and pagination
        keyboard = create_orders_list_keyboard(
            orders,
            current_page,
            total_pages,
            order_status
        )

        await callback_query.message.edit_text(
            f"📋 Заказы со статусом {ORDER_STATUS[order_status]}\n"
            f"Страница {current_page} из {total_pages} "
            f"(Всего заказов: {total_count})",
            reply_markup=keyboard
        )
        await callback_query.answer()


    except Exception as e:
        await callback_query.message.edit_text(f"❌ Ошибка: {str(e)}")
        await callback_query.answer()




# Common utility for both orders and workers
def get_current_page_from_message(message_text: Optional[str]) -> int:
    """Extract current page number from message text."""
    if not message_text:
        return 1

    try:
        page_part = message_text.split("Страница")
        if len(page_part) < 2:
            return 1

        page_number = page_part[1].split("из")[0].strip()
        return int(page_number)
    except (IndexError, ValueError):
        return 1


# Add remaining handler for current page button
@orders_router.callback_query(F.data == "current_page")
async def handle_current_page(callback_query: CallbackQuery):
    """Handle current page button press."""
    await callback_query.answer("Текущая страница")
