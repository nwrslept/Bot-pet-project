from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="👤 Профіль")],
        [KeyboardButton(text="🤖 Чат з Gemini"), KeyboardButton(text="💡 Згенерувати ідею")],
        [KeyboardButton(text="📰 Новини")],

    ], resize_keyboard=True)

def gemini_left_chat():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🚪 Покинути чат")],
    ], resize_keyboard=True)
