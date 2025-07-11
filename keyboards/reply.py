from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lang.messages import t

def main_menu_keyboard(lang: str):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(lang, "menu_profile"))],
            [KeyboardButton(text=t(lang, "menu_language"))],
            [KeyboardButton(text=t(lang, "menu_chat_gemini")), KeyboardButton(text=t(lang, "menu_generate_idea"))],
            [KeyboardButton(text=t(lang, "menu_news")), KeyboardButton(text="🎮 Steam")]

        ],
        resize_keyboard=True
    )

def gemini_left_chat(lang: str):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(lang, "button_leave_chat"))],
        ],
        resize_keyboard=True
    )
