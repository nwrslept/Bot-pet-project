from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def idea_topic_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🤖 Телеграм-бот", callback_data="topic:telegram"),
            InlineKeyboardButton(text="🕷️ Скрейпер", callback_data="topic:scraper"),
        ],
        [
            InlineKeyboardButton(text="📊 Аналітика", callback_data="topic:analytics"),
            InlineKeyboardButton(text="🎮 Гра", callback_data="topic:game"),
        ],
        [
            InlineKeyboardButton(text="🧰 Утиліта", callback_data="topic:utility"),
            InlineKeyboardButton(text="🧠 Нейронка", callback_data="topic:neural"),
        ],
    ])

def idea_difficulty_keyboard(topic: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🟢 Легка", callback_data=f"idea:{topic}:easy"),
            InlineKeyboardButton(text="🟡 Середня", callback_data=f"idea:{topic}:medium"),
            InlineKeyboardButton(text="🔴 Складна", callback_data=f"idea:{topic}:hard"),
        ]
    ])
