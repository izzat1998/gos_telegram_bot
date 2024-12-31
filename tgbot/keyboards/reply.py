from typing import Dict, List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



def create_specialization_keyboard(specializations: List[Dict]) -> ReplyKeyboardMarkup:
    """Create keyboard for specializations list."""
    keyboard = []
    
    # Add specialization buttons (2 per row)
    for i in range(0, len(specializations), 2):
        row = [KeyboardButton(text=specializations[i]['name'])]
        if i + 1 < len(specializations):
            row.append(KeyboardButton(text=specializations[i + 1]['name']))
        keyboard.append(row)
    
    # Add a "Back" button at the bottom
    keyboard.append([KeyboardButton(text="Все Мастера")])
    keyboard.append([KeyboardButton(text="⬅️ Назад")])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


