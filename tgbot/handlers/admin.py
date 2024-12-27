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
    buttons = [[KeyboardButton(text="📊 Статистика заказов")]]

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons, resize_keyboard=True, one_time_keyboard=False
    )

    await message.reply("Здравствуйте, админ!", reply_markup=keyboard)


@admin_router.callback_query(F.data == "current_page")
async def handle_current_page(callback_query: CallbackQuery):
    await callback_query.answer("Текущая страница")


@admin_router.callback_query(F.data == "back_to_stats")
async def back_to_statistics(callback_query: CallbackQuery, state: FSMContext):
    if not callback_query.message or not isinstance(callback_query.message, Message):
        await callback_query.answer("Cannot process this action")
        return

    await get_order_statistics(callback_query.message, state)
    await callback_query.answer()


@admin_router.message(F.text == "📊 Статистика заказов")
async def get_order_statistics(message: Message, state: FSMContext):
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

        inline_buttons = [
            [
                InlineKeyboardButton(
                    text=f"✅ Подтверждено: {status_counts['approved']}",
                    callback_data="approved",
                ),
                InlineKeyboardButton(
                    text=f"❌ Отменено: {status_counts['cancelled']}",
                    callback_data="cancelled",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"⭐ Завершено: {status_counts['completed']}",
                    callback_data="completed",
                ),
                InlineKeyboardButton(
                    text=f"🏭 В производстве: {status_counts['in_production']}",
                    callback_data="in_production",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"🔨 Установка: {status_counts['installation_in_progress']}",
                    callback_data="installation_in_progress",
                ),
                InlineKeyboardButton(
                    text=f"👀 На рассмотрении: {status_counts['pending_review']}",
                    callback_data="pending_review",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"📦 Готово к установке: {status_counts['ready_for_installation']}",
                    callback_data="ready_for_installation",
                ),
                InlineKeyboardButton(
                    text=f"👷 Назначен работник: {status_counts['worker_assigned']}",
                    callback_data="worker_assigned",
                ),
            ],
        ]

        inline_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_buttons)
        await state.set_state(OrderStatistics.list_by_status)
        await message.reply(response, parse_mode="HTML", reply_markup=inline_keyboard)

    except Exception as e:
        await message.reply(f"Error: {str(e)}")


def get_current_page_from_message(message_text: Optional[str]) -> int:
    """Extract current page number from message text with proper error handling."""
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


@admin_router.callback_query(F.data.startswith("order:"))
async def get_order_detail(callback_query: CallbackQuery):
    if not callback_query.message and not callback_query:
        await callback_query.answer("Cannot process this request")
        return

    if not isinstance(callback_query.message, Message):
        await callback_query.answer("Cannot edit this message")
        return

    current_page = get_current_page_from_message(callback_query.message.text)
    order_id = callback_query.data.split(":")[1]
    api_client = APIClient()

    try:
        order = await api_client.get_order_detail(order_id)

        workers_info = []
        for worker in order["assigned_workers"]:
            workers_info.append(
                f"👤 <b>{worker['name']}</b>\n"
                f"   ⭐️ Рейтинг: {worker['rating']}\n"
                f"   🗓 Опыт: {worker['experience_years']} лет\n"
            )

        def format_created_at(datetime_str: str) -> str:
            dt = datetime.fromisoformat(datetime_str)
            return dt.strftime("%d %B %Y, %H:%M")

        def format_deadline(datetime_str: str) -> str:
            dt = datetime.fromisoformat(datetime_str)
            return dt.strftime("%d %B %Y")

        response = (
            f"🔸 <b>Заказ #{order_id}</b>\n\n"
            f"📅 <b>Создан:</b> {format_created_at(order['created_at'])}\n"
            f"📦 <b>Статус:</b> {ORDER_STATUS[order['status']]}\n"
            f"💵 <b>Стоимость:</b> {order['price']}$\n"
            f"🕒 <b>Дедлайн:</b> {format_deadline(order['deadline'])}\n\n"
            f"📍 <b>Адрес установки:</b>\n"
            f"   {order['installation_address']}\n\n"
            f"📝 <b>Описание:</b>\n"
            f"   {order['description']}\n\n"
            f"👥 <b>Исполнители:</b>\n"
            f"{''.join(workers_info)}"
        )

        back_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🔙 Назад к списку",
                        callback_data=f"{order['status']}:next:{current_page}",
                    )
                ]
            ]
        )

        await callback_query.message.edit_text(
            response, parse_mode="HTML", reply_markup=back_button
        )
    except Exception as e:
        await callback_query.message.edit_text(f"❌ Ошибка: {str(e)}")


@admin_router.callback_query(OrderStatistics.list_by_status)
async def get_order_list_by_status(callback_query: CallbackQuery):
    if not callback_query.message:
        await callback_query.answer("Cannot process this request")
        return

    if not isinstance(callback_query.message, Message):
        await callback_query.answer("Cannot edit this message")
        return

    data_parts = callback_query.data.split(":")
    api_client = APIClient()

    try:
        if len(data_parts) == 1:
            order_status = data_parts[0]
            response = await api_client.get_order_list_by_status(order_status)
            current_page = 1
        else:
            order_status = data_parts[0]
            page = int(data_parts[2])
            response = await api_client.get_order_list_by_status(
                order_status, page=page
            )
            current_page = page

        orders = response.get("results", [])
        total_count = response.get("count", 0)
        next_url = response.get("next")
        prev_url = response.get("previous")

        total_pages = (total_count + 9) // 10

        order_buttons = []
        for i in range(0, len(orders), 2):
            row = []
            row.append(
                InlineKeyboardButton(
                    text=f"📋 {orders[i]['order_id']}",
                    callback_data=f"order:{orders[i]['order_id']}",
                )
            )
            if i + 1 < len(orders):
                row.append(
                    InlineKeyboardButton(
                        text=f"📋 {orders[i + 1]['order_id']}",
                        callback_data=f"order:{orders[i + 1]['order_id']}",
                    )
                )
            order_buttons.append(row)

        pagination_buttons = []

        if prev_url:
            pagination_buttons.append(
                InlineKeyboardButton(
                    text="⬅️ Предыдущая",
                    callback_data=f"{order_status}:prev:{current_page - 1}",
                )
            )

        pagination_buttons.append(
            InlineKeyboardButton(
                text=f"📄 {current_page}/{total_pages}", callback_data="current_page"
            )
        )

        if next_url:
            pagination_buttons.append(
                InlineKeyboardButton(
                    text="➡️ Следующая",
                    callback_data=f"{order_status}:next:{current_page + 1}",
                )
            )

        back_button = [
            [
                InlineKeyboardButton(
                    text="🔙 Назад к статистике", callback_data="back_to_stats"
                )
            ]
        ]

        all_buttons = order_buttons + [pagination_buttons] + back_button
        keyboard = InlineKeyboardMarkup(inline_keyboard=all_buttons)

        await callback_query.message.edit_text(
            f"📋 Заказы со статусом {ORDER_STATUS[order_status]}\n"
            f"Страница {current_page} из {total_pages} (Всего заказов: {total_count})",
            reply_markup=keyboard,
        )

    except Exception as e:
        await callback_query.message.edit_text(f"Error: {str(e)}")
