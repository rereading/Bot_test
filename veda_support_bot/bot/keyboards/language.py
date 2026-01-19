from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def language_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора языка"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz")
        ],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
    ])