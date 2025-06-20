from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def idea_difficulty_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🟢 Легка", callback_data="idea:easy"),
            InlineKeyboardButton(text="🟡 Середня", callback_data="idea:medium"),
            InlineKeyboardButton(text="🔴 Складна", callback_data="idea:hard"),
        ]
    ])
