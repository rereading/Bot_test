from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List
from bot.models.filial import Filial


def filials_keyboard(filials: List[Filial]) -> InlineKeyboardMarkup:
    """Клавиатура выбора филиала"""
    buttons = []
    
    for filial in filials:
        buttons.append([
            InlineKeyboardButton(
                text=filial.name,
                callback_data=f"filial_{filial.id}"
            )
        ])
    
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)