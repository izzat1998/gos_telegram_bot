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
    buttons = [[KeyboardButton(text="📊 Статистика заказов"),
                KeyboardButton(text="Мастера")]]

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons, resize_keyboard=True, one_time_keyboard=False
    )

    await message.reply("Здравствуйте, админ!", reply_markup=keyboard)

#
# @admin_router.callback_query(F.data == "current_page")
# async def handle_current_page(callback_query: CallbackQuery):
#     await callback_query.answer("Текущая страница")
#
#
# @admin_router.callback_query(F.data == "back_to_stats")
# async def back_to_statistics(callback_query: CallbackQuery, state: FSMContext):
#     if not callback_query.message or not isinstance(callback_query.message, Message):
#         await callback_query.answer("Cannot process this action")
#         return
#
#     api_client = APIClient()
#     try:
#         statistics = await api_client.get_order_statistics()
#         status_dist = statistics["status_distribution"]
#         finance = statistics["finance_stats"]
#         status_counts = {item["status"]: item["count"] for item in status_dist}
#
#         response = (
#             "📈 <b>Финансовая статистика</b>\n"
#             f"💰 Общая выручка: {finance['total_revenue']}$\n"
#             f"📦 Всего заказов: {finance['total_orders']}\n"
#             f"💎 Средний чек: {finance['avg_order_value']}$\n\n"
#         )
#
#         inline_buttons = [
#             [
#                 InlineKeyboardButton(
#                     text=f"✅ Подтверждено: {status_counts['approved']}",
#                     callback_data="approved",
#                 ),
#                 InlineKeyboardButton(
#                     text=f"❌ Отменено: {status_counts['cancelled']}",
#                     callback_data="cancelled",
#                 ),
#             ],
#             [
#                 InlineKeyboardButton(
#                     text=f"⭐ Завершено: {status_counts['completed']}",
#                     callback_data="completed",
#                 ),
#                 InlineKeyboardButton(
#                     text=f"🏭 В производстве: {status_counts['in_production']}",
#                     callback_data="in_production",
#                 ),
#             ],
#             [
#                 InlineKeyboardButton(
#                     text=f"🔨 Установка: {status_counts['installation_in_progress']}",
#                     callback_data="installation_in_progress",
#                 ),
#                 InlineKeyboardButton(
#                     text=f"👀 На рассмотрении: {status_counts['pending_review']}",
#                     callback_data="pending_review",
#                 ),
#             ],
#             [
#                 InlineKeyboardButton(
#                     text=f"📦 Готово к установке: {status_counts['ready_for_installation']}",
#                     callback_data="ready_for_installation",
#                 ),
#                 InlineKeyboardButton(
#                     text=f"👷 Назначен работник: {status_counts['worker_assigned']}",
#                     callback_data="worker_assigned",
#                 ),
#             ],
#         ]
#
#         inline_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_buttons)
#         await state.set_state(OrderStatistics.list_by_status)
#         await callback_query.message.edit_text(
#             response, parse_mode="HTML", reply_markup=inline_keyboard
#         )
#         await callback_query.answer()
#
#     except Exception as e:
#         await callback_query.message.edit_text(f"Error: {str(e)}")
#
#
# @admin_router.message(F.text == "📊 Статистика заказов")
# async def get_order_statistics(message: Message, state: FSMContext):
#     api_client = APIClient()
#     try:
#         statistics = await api_client.get_order_statistics()
#         status_dist = statistics["status_distribution"]
#         finance = statistics["finance_stats"]
#         status_counts = {item["status"]: item["count"] for item in status_dist}
#
#         response = (
#             "📈 <b>Финансовая статистика</b>\n"
#             f"💰 Общая выручка: {finance['total_revenue']}$\n"
#             f"📦 Всего заказов: {finance['total_orders']}\n"
#             f"💎 Средний чек: {finance['avg_order_value']}$\n\n"
#         )
#
#         inline_buttons = [
#             [
#                 InlineKeyboardButton(
#                     text=f"✅ Подтверждено: {status_counts['approved']}",
#                     callback_data="approved",
#                 ),
#                 InlineKeyboardButton(
#                     text=f"❌ Отменено: {status_counts['cancelled']}",
#                     callback_data="cancelled",
#                 ),
#             ],
#             [
#                 InlineKeyboardButton(
#                     text=f"⭐ Завершено: {status_counts['completed']}",
#                     callback_data="completed",
#                 ),
#                 InlineKeyboardButton(
#                     text=f"🏭 В производстве: {status_counts['in_production']}",
#                     callback_data="in_production",
#                 ),
#             ],
#             [
#                 InlineKeyboardButton(
#                     text=f"🔨 Установка: {status_counts['installation_in_progress']}",
#                     callback_data="installation_in_progress",
#                 ),
#                 InlineKeyboardButton(
#                     text=f"👀 На рассмотрении: {status_counts['pending_review']}",
#                     callback_data="pending_review",
#                 ),
#             ],
#             [
#                 InlineKeyboardButton(
#                     text=f"📦 Готово к установке: {status_counts['ready_for_installation']}",
#                     callback_data="ready_for_installation",
#                 ),
#                 InlineKeyboardButton(
#                     text=f"👷 Назначен работник: {status_counts['worker_assigned']}",
#                     callback_data="worker_assigned",
#                 ),
#             ],
#         ]
#
#         inline_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_buttons)
#         await state.set_state(OrderStatistics.list_by_status)
#         await message.reply(response, parse_mode="HTML", reply_markup=inline_keyboard)
#
#     except Exception as e:
#         await message.reply(f"Error: {str(e)}")
#
#
# def get_current_page_from_message(message_text: Optional[str]) -> int:
#     """Extract current page number from message text with proper error handling."""
#     if not message_text:
#         return 1
#
#     try:
#         page_part = message_text.split("Страница")
#         if len(page_part) < 2:
#             return 1
#
#         page_number = page_part[1].split("из")[0].strip()
#         return int(page_number)
#     except (IndexError, ValueError):
#         return 1
#
#
# @admin_router.callback_query(F.data.startswith("order:"))
# async def get_order_detail(callback_query: CallbackQuery):
#     if not callback_query.message and not callback_query:
#         await callback_query.answer("Cannot process this request")
#         return
#
#     if not isinstance(callback_query.message, Message):
#         await callback_query.answer("Cannot edit this message")
#         return
#
#     current_page = get_current_page_from_message(callback_query.message.text)
#     order_id = callback_query.data.split(":")[1]
#     api_client = APIClient()
#
#     try:
#         order = await api_client.get_order_detail(order_id)
#
#         workers_info = []
#         for worker in order["assigned_workers"]:
#             workers_info.append(
#                 f"👤 <b>{worker['name']}</b>\n"
#                 f"   ⭐️ Рейтинг: {worker['rating']}\n"
#                 f"   🗓 Опыт: {worker['experience_years']} лет\n"
#             )
#
#         def format_created_at(datetime_str: str) -> str:
#             dt = datetime.fromisoformat(datetime_str)
#             return dt.strftime("%d %B %Y, %H:%M")
#
#         def format_deadline(datetime_str: str) -> str:
#             dt = datetime.fromisoformat(datetime_str)
#             return dt.strftime("%d %B %Y")
#
#         response = (
#             f"🔸 <b>Заказ #{order_id}</b>\n\n"
#             f"📅 <b>Создан:</b> {format_created_at(order['created_at'])}\n"
#             f"📦 <b>Статус:</b> {ORDER_STATUS[order['status']]}\n"
#             f"💵 <b>Стоимость:</b> {order['price']}$\n"
#             f"🕒 <b>Дедлайн:</b> {format_deadline(order['deadline'])}\n\n"
#             f"📍 <b>Адрес установки:</b>\n"
#             f"   {order['installation_address']}\n\n"
#             f"📝 <b>Описание:</b>\n"
#             f"   {order['description']}\n\n"
#             f"👥 <b>Исполнители:</b>\n"
#             f"{''.join(workers_info)}"
#         )
#
#         back_button = InlineKeyboardMarkup(
#             inline_keyboard=[
#                 [
#                     InlineKeyboardButton(
#                         text="🔙 Назад к списку",
#                         callback_data=f"{order['status']}:next:{current_page}",
#                     )
#                 ]
#             ]
#         )
#
#         await callback_query.message.edit_text(
#             response, parse_mode="HTML", reply_markup=back_button
#         )
#     except Exception as e:
#         await callback_query.message.edit_text(f"❌ Ошибка: {str(e)}")
#
#
# @admin_router.callback_query(OrderStatistics.list_by_status)
# async def get_order_list_by_status(callback_query: CallbackQuery):
#     if not callback_query.message:
#         await callback_query.answer("Cannot process this request")
#         return
#
#     if not isinstance(callback_query.message, Message):
#         await callback_query.answer("Cannot edit this message")
#         return
#
#     data_parts = callback_query.data.split(":")
#     api_client = APIClient()
#
#     try:
#         if len(data_parts) == 1:
#             order_status = data_parts[0]
#             response = await api_client.get_order_list_by_status(order_status)
#             current_page = 1
#         else:
#             order_status = data_parts[0]
#             page = int(data_parts[2])
#             response = await api_client.get_order_list_by_status(
#                 order_status, page=page
#             )
#             current_page = page
#
#         orders = response.get("results", [])
#         total_count = response.get("count", 0)
#         next_url = response.get("next")
#         prev_url = response.get("previous")
#
#         total_pages = (total_count + 9) // 10
#
#         order_buttons = []
#         for i in range(0, len(orders), 2):
#             row = []
#             row.append(
#                 InlineKeyboardButton(
#                     text=f"📋 {orders[i]['order_id']}",
#                     callback_data=f"order:{orders[i]['order_id']}",
#                 )
#             )
#             if i + 1 < len(orders):
#                 row.append(
#                     InlineKeyboardButton(
#                         text=f"📋 {orders[i + 1]['order_id']}",
#                         callback_data=f"order:{orders[i + 1]['order_id']}",
#                     )
#                 )
#             order_buttons.append(row)
#
#         pagination_buttons = []
#
#         if prev_url:
#             pagination_buttons.append(
#                 InlineKeyboardButton(
#                     text="⬅️ Предыдущая",
#                     callback_data=f"{order_status}:prev:{current_page - 1}",
#                 )
#             )
#
#         pagination_buttons.append(
#             InlineKeyboardButton(
#                 text=f"📄 {current_page}/{total_pages}", callback_data="current_page"
#             )
#         )
#
#         if next_url:
#             pagination_buttons.append(
#                 InlineKeyboardButton(
#                     text="➡️ Следующая",
#                     callback_data=f"{order_status}:next:{current_page + 1}",
#                 )
#             )
#
#         back_button = [
#             [
#                 InlineKeyboardButton(
#                     text="🔙 Назад к статистике", callback_data="back_to_stats"
#                 )
#             ]
#         ]
#
#         all_buttons = order_buttons + [pagination_buttons] + back_button
#         keyboard = InlineKeyboardMarkup(inline_keyboard=all_buttons)
#
#         await callback_query.message.edit_text(
#             f"📋 Заказы со статусом {ORDER_STATUS[order_status]}\n"
#             f"Страница {current_page} из {total_pages} (Всего заказов: {total_count})",
#             reply_markup=keyboard,
#         )
#
#     except Exception as e:
#         await callback_query.message.edit_text(f"Error: {str(e)}")
#
#
# @admin_router.message(F.text == "Мастера")
# async def get_workers_list(message: Message):
#     api_client = APIClient()
#     try:
#         # Get first page of workers
#         response = await api_client.get_workers(page=1)
#         workers = response.get("results", [])
#         total_count = response.get("count", 0)
#         total_pages = (total_count + 9) // 10
#         current_page = 1
#
#         # Create formatted text for workers list
#         text = _format_workers_list_header()
#
#         for worker in workers:
#             text += _format_worker_info(worker)
#             text += _format_worker_orders(worker)
#             text += _format_worker_specializations(worker)
#             text += "━━━━━━━━━━━━━━━━━━━━━━\n"
#
#         text += _format_pagination_info(current_page, total_pages, total_count)
#
#         # Create pagination keyboard
#         keyboard = _create_pagination_keyboard(current_page, total_pages)
#
#         await message.reply(text, reply_markup=keyboard, parse_mode="HTML")
#
#     except Exception as e:
#         await message.reply(f"Errorrrrs: {str(e)}")
#
#
# def _format_workers_list_header() -> str:
#     """Format the header for the workers list."""
#     return (
#         "👷 <b>Список мастеров</b>\n"
#         "━━━━━━━━━━━━━━━━━━━━━━\n"
#     )
#
#
# def _format_worker_info(worker: dict) -> str:
#     """Format basic worker information."""
#     availability_status = "🟢 Свободен" if worker['is_available'] else "🔴 Занят"
#
#     return (
#         f"👤 <b>{worker['name']}</b>\n"
#         f"⭐️ Рейтинг: {worker['rating']}\n"
#         f"🗓 Опыт: {worker['experience_years']} лет\n"
#         f"📍 <b>Адрес:</b> {worker['address']}\n"
#         f"📞 <b>Телефон:</b> {worker['phone_number']}\n"
#         f"{availability_status}\n"
#     )
#
#
# def _format_worker_orders(worker: dict) -> str:
#     """Format worker's assigned orders."""
#     if not worker.get("assigned_orders"):
#         return "📦 Назначенные заказы: нет\n"
#
#     orders_text = "📦 Назначенные заказы:\n"
#     for order in worker["assigned_orders"]:
#         orders_text += f"  • <code>{order['order_id']}</code>\n"
#     return orders_text
#
#
# def _format_worker_specializations(worker: dict) -> str:
#     """Format worker's specializations."""
#     if not worker.get("specializations"):
#         return "🛠 Специализации: нет\n"
#
#     specs_text = "🛠 Специализации:\n"
#     for spec in worker["specializations"]:
#         specs_text += f"  • <code>{spec['name']}</code>\n"
#     return specs_text
#
#
# def _format_pagination_info(current_page: int, total_pages: int, total_count: int) -> str:
#     """Format pagination information."""
#     return (
#         f"📄 Страница {current_page} из {total_pages}\n"
#         f"📊 Всего специалистов: {total_count}"
#     )
#
#
# def _create_pagination_keyboard(current_page: int, total_pages: int) -> InlineKeyboardMarkup:
#     """Create pagination keyboard with navigation buttons."""
#     buttons = []
#
#     # Previous page button
#     if current_page > 1:
#         buttons.append(
#             InlineKeyboardButton(
#                 text="⬅️ Предыдущая",
#                 callback_data=f"workers:prev:{current_page - 1}"
#             )
#         )
#
#     # Current page indicator
#     buttons.append(
#         InlineKeyboardButton(
#             text=f"📄 {current_page}/{total_pages}",
#             callback_data="current_page"
#         )
#     )
#
#     # Next page button
#     if current_page < total_pages:
#         buttons.append(
#             InlineKeyboardButton(
#                 text="➡️ Следующая",
#                 callback_data=f"workers:next:{current_page + 1}"
#             )
#         )
#
#     return InlineKeyboardMarkup(inline_keyboard=[buttons])
#
#
# @admin_router.callback_query(F.data.startswith("workers"))
# async def paginate_workers(callback_query: CallbackQuery):
#     """Handle pagination for workers list."""
#     if not callback_query.message:
#         await callback_query.answer("Cannot process this request")
#         return
#
#     if not isinstance(callback_query.message, Message):
#         await callback_query.answer("Cannot edit this message")
#         return
#
#     api_client = APIClient()
#     data_parts = callback_query.data.split(":")
#
#     try:
#         # Parse page number from callback data
#         page = int(data_parts[2])
#
#         # Get workers for requested page
#         response = await api_client.get_workers(page=page)
#         workers = response.get("results", [])
#         total_count = response.get("count", 0)
#         total_pages = (total_count + 9) // 10
#
#         # Format the complete message
#         text = _format_workers_list_header()
#
#         for worker in workers:
#             text += _format_worker_info(worker)
#             text += _format_worker_orders(worker)
#             text += _format_worker_specializations(worker)
#             text += "━━━━━━━━━━━━━━━━━━━━━━\n"
#
#         text += _format_pagination_info(page, total_pages, total_count)
#
#         # Create pagination keyboard
#         keyboard = _create_pagination_keyboard(page, total_pages)
#
#         await callback_query.message.edit_text(
#             text,
#             reply_markup=keyboard,
#             parse_mode="HTML"
#         )
#
#     except Exception as e:
#         await callback_query.message.edit_text(f"Errorrrr: {str(e)}")
#
#
# @admin_router.callback_query(F.data == "current_page")
# async def handle_current_page(callback_query: CallbackQuery):
#     """Handle clicks on the current page button."""
#     await callback_query.answer("Текущая страница")