from typing import Dict, List


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



# This is a simple keyboard, that contains 2 buttons
def create_pagination_keyboard(
    current_page: int,
    total_pages: int,
    prefix: str
) -> InlineKeyboardMarkup:
    """Create pagination keyboard for lists."""
    buttons = []
    row = []

    if current_page > 1:
        row.append(
            InlineKeyboardButton(
                text="⬅️ Предыдущая",
                callback_data=f"{prefix}:prev:{current_page - 1}"
            )
        )

    row.append(
        InlineKeyboardButton(
            text=f"📄 {current_page}/{total_pages}",
            callback_data="current_page"
        )
    )

    if current_page < total_pages:
        row.append(
            InlineKeyboardButton(
                text="➡️ Следующая",
                callback_data=f"{prefix}:next:{current_page + 1}"
            )
        )

    buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def create_statistics_keyboard(status_counts: Dict[str, int]) -> InlineKeyboardMarkup:
    """Create keyboard for order statistics."""
    buttons = [
        [
            InlineKeyboardButton(
                text=f"✅ Подтверждено: {status_counts['approved']}",
                callback_data="approved"
            ),
            InlineKeyboardButton(
                text=f"❌ Отменено: {status_counts['cancelled']}",
                callback_data="cancelled"
            )
        ],
        [
            InlineKeyboardButton(
                text=f"⭐ Завершено: {status_counts['completed']}",
                callback_data="completed"
            ),
            InlineKeyboardButton(
                text=f"🏭 В производстве: {status_counts['in_production']}",
                callback_data="in_production"
            )
        ],
        [
            InlineKeyboardButton(
                text=f"🔨 Установка: {status_counts['installation_in_progress']}",
                callback_data="installation_in_progress"
            ),
            InlineKeyboardButton(
                text=f"👀 На рассмотрении: {status_counts['pending_review']}",
                callback_data="pending_review"
            )
        ],
        [
            InlineKeyboardButton(
                text=f"📦 Готово к установке: {status_counts['ready_for_installation']}",
                callback_data="ready_for_installation"
            ),
            InlineKeyboardButton(
                text=f"👷 Назначен работник: {status_counts['worker_assigned']}",
                callback_data="worker_assigned"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_orders_list_keyboard(
        orders: List[Dict],
        current_page: int,
        total_pages: int,
        status: str
) -> InlineKeyboardMarkup:
    """Create keyboard for orders list with pagination."""
    buttons = []

    # Order buttons (2 per row)
    for i in range(0, len(orders), 2):
        row = [
            InlineKeyboardButton(
                text=f"📋 {orders[i]['order_id']}",
                callback_data=f"order:{orders[i]['order_id']}"
            )
        ]
        if i + 1 < len(orders):
            row.append(
                InlineKeyboardButton(
                    text=f"📋 {orders[i + 1]['order_id']}",
                    callback_data=f"order:{orders[i + 1]['order_id']}"
                )
            )
        buttons.append(row)

    # Pagination row
    pagination_row = []
    if current_page > 1:
        pagination_row.append(
            InlineKeyboardButton(
                text="⬅️ Предыдущая",
                callback_data=f"{status}:prev:{current_page - 1}"
            )
        )

    pagination_row.append(
        InlineKeyboardButton(
            text=f"📄 {current_page}/{total_pages}",
            callback_data="current_page"
        )
    )

    if current_page < total_pages:
        pagination_row.append(
            InlineKeyboardButton(
                text="➡️ Следующая",
                callback_data=f"{status}:next:{current_page + 1}"
            )
        )

    buttons.append(pagination_row)

    # Back button
    buttons.append([
        InlineKeyboardButton(
            text="🔙 Назад к статистике",
            callback_data="back_to_stats"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def type_of_worker_keyboard() -> InlineKeyboardMarkup:
    """Create inline keyboard for worker type selection."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👨‍🔧 Мастера", callback_data="workers")],
            [InlineKeyboardButton(text="👨‍🔧 Верифицированные мастера ", callback_data="verified_workers")],
        ]
    )


# Callback data prefixes
SPECIALIZATION_PREFIX = "spec"
PAGINATION_PREFIX = "workers"

# Callback actions
ACTION_ALL = "all"
ACTION_BACK = "back"

def create_specialization_inline_keyboard(specializations: List[Dict]) -> InlineKeyboardMarkup:
    """
    Create inline keyboard for specializations list.
    
    Args:
        specializations: List of specialization dictionaries with 'name' and 'slug' keys
        
    Returns:
        InlineKeyboardMarkup: Keyboard with specialization buttons
    """
    buttons = []
    # Add "All Masters" button
    buttons.append([InlineKeyboardButton(
        text="👥 Все Мастера",
        callback_data=f"{SPECIALIZATION_PREFIX}:{ACTION_ALL}"
    )])
    
    # Add specialization buttons in pairs
    spec_buttons = []
    for spec in specializations:
        spec_buttons.append(InlineKeyboardButton(
            text=f"👤 {spec['name']}",
            callback_data=f"{SPECIALIZATION_PREFIX}:{spec['slug']}"
        ))
        
        # Add row after every 2 buttons
        if len(spec_buttons) == 2:
            buttons.append(spec_buttons)
            spec_buttons = []
    
    # Add remaining buttons if any
    if spec_buttons:
        buttons.append(spec_buttons)


    return InlineKeyboardMarkup(inline_keyboard=buttons)