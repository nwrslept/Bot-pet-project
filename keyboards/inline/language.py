from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇦 Українська", callback_data="lang:uk"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en"),
        ]
    ])
