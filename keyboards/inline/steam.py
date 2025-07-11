from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def steam_menu_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 Мій профіль", callback_data="steam_profile")],
        [InlineKeyboardButton(text="✏️ Змінити посилання", callback_data="steam_change")],
        [InlineKeyboardButton(text="👥 Список друзів", callback_data="steam_friends")]
    ])
    return keyboard

def back_to_steam_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад до меню", callback_data="steam_back")]
    ])
