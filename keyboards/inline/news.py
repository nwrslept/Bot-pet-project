from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def news_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔍 Переглянути", callback_data="news:browse")],
        [InlineKeyboardButton(text="📩 Підписатися", callback_data="subscribe:news")]
    ])

def news_topics_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏛️ Політика", callback_data="news:politics")],
        [InlineKeyboardButton(text="⚽ Спорт", callback_data="news:sports")],
        [InlineKeyboardButton(text="💻 Технології", callback_data="news:technology")],
        [InlineKeyboardButton(text="🩺 Здоров’я", callback_data="news:health")],
        [InlineKeyboardButton(text="🎉 Розваги", callback_data="news:entertainment")],
        [InlineKeyboardButton(text="⬅ Назад", callback_data="menu:back")],
    ])

def news_action_keyboard(topic: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Ще 📰", callback_data=f"more:{topic}")],
        [InlineKeyboardButton(text="⬅ Назад", callback_data="back:topics")],
    ])
