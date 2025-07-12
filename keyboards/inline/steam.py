from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from lang.messages import t
from database.subscriptions import is_user_steam_subscribed

def steam_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "steam.menu.profile"), callback_data="steam_profile")],
        [InlineKeyboardButton(text=t(lang, "steam.menu.change"), callback_data="steam_change")],
        [InlineKeyboardButton(text=t(lang, "steam.menu.friends"), callback_data="steam_friends")],
        [InlineKeyboardButton(text=t(lang, "steam.menu.free_games"), callback_data="steam_free_games")]
    ])
    return keyboard


def steam_free_games_menu(lang: str, telegram_id: int) -> InlineKeyboardMarkup:
    subscribed = is_user_steam_subscribed(telegram_id)
    subscribe_text = (
        f"{t(lang, 'steam.menu.subscribe_free')} {'✅' if subscribed else '❌'}"
    )
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "steam.menu.random_free"), callback_data="steam_random_free")],
        [InlineKeyboardButton(text=subscribe_text, callback_data="steam_subscribe_free")],
        [InlineKeyboardButton(text=t(lang, "steam.menu.back"), callback_data="steam_back")]
    ])


def back_to_steam_menu(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "steam.menu.back"), callback_data="steam_back")]
    ])
