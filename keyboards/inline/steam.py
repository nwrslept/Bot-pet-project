from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from lang.messages import t

def steam_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "steam.menu.profile"), callback_data="steam_profile")],
        [InlineKeyboardButton(text=t(lang, "steam.menu.change"), callback_data="steam_change")],
        [InlineKeyboardButton(text=t(lang, "steam.menu.friends"), callback_data="steam_friends")]
    ])
    return keyboard


def back_to_steam_menu(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "steam.menu.back"), callback_data="steam_back")]
    ])
