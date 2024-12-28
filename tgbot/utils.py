from datetime import datetime
from typing import Dict, List
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ITEMS_PER_PAGE = 10
ORDER_STATUS = {
    "pending_review": "Ожидает проверки",
    "approved": "Одобрено",
    "worker_assigned": "Назначен исполнитель",
    "in_production": "В производстве",
    "ready_for_installation": "Готово к установке",
    "installation_in_progress": "Установка в процессе",
    "completed": "Завершено",
    "cancelled": "Отменено",
}
def format_worker_list(workers: List[Dict]) -> str:
    """Format workers list into readable text."""
    text = "👷 <b>Список мастеров</b>\n"
    text += "━━━━━━━━━━━━━━━━━━━━━━\n"

    for worker in workers:
        # Basic info
        text += (
            f"👤 <b>{worker['name']}</b>\n"
            f"⭐️ Рейтинг: {worker['rating']}\n"
            f"🗓 Опыт: {worker['experience_years']} лет\n"
            f"📍 <b>Адрес:</b> {worker['address']}\n"
            f"📞 <b>Телефон:</b> {worker['phone_number']}\n"
            f"{'🟢 Свободен' if worker['is_available'] else '🔴 Занят'}\n"
        )

        # Orders
        if worker.get("assigned_orders"):
            text += "📦 Назначенные заказы:\n"
            text += "".join(
                f"  • <code>{order['order_id']}</code>\n"
                for order in worker["assigned_orders"]
            )
        else:
            text += "📦 Назначенные заказы: нет\n"

        # Specializations
        if worker.get("specializations"):
            text += "🛠 Специализации:\n"
            text += "".join(
                f"  • <code>{spec['name']}</code>\n"
                for spec in worker["specializations"]
            )
        else:
            text += "🛠 Специализации: нет\n"

        text += "━━━━━━━━━━━━━━━━━━━━━━\n"

    return text




def format_datetime(dt_str: str, include_time: bool = True) -> str:
    """Format datetime string to human-readable format."""
    dt = datetime.fromisoformat(dt_str)
    return dt.strftime("%d %B %Y, %H:%M") if include_time else dt.strftime("%d %B %Y")

def format_order_detail(order: Dict) -> str:
    """Format single order details."""
    workers_info = []
    for worker in order["assigned_workers"]:
        workers_info.append(
            f"👤 <b>{worker['name']}</b>\n"
            f"   ⭐️ Рейтинг: {worker['rating']}\n"
            f"   🗓 Опыт: {worker['experience_years']} лет\n"
        )

    return (
        f"🔸 <b>Заказ #{order['order_id']}</b>\n\n"  # Changed from 'id' to 'order_id'
        f"📅 <b>Создан:</b> {format_datetime(order['created_at'])}\n"
        f"📦 <b>Статус:</b> {ORDER_STATUS[order['status']]}\n"
        f"💵 <b>Стоимость:</b> {order['price']}$\n"
        f"🕒 <b>Дедлайн:</b> {format_datetime(order['deadline'], False)}\n\n"
        f"📍 <b>Адрес установки:</b>\n"
        f"   {order['installation_address']}\n\n"
        f"📝 <b>Описание:</b>\n"
        f"   {order['description']}\n\n"
        f"👥 <b>Исполнители:</b>\n"
        f"{''.join(workers_info)}"
    )