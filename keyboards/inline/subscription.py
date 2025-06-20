from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def subscription_menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Частота", callback_data="sub:frequency")],
        [InlineKeyboardButton(text="📚 Теми", callback_data="sub:topics")],
        [InlineKeyboardButton(text="❌ Відписатись", callback_data="sub:unsubscribe")],
        [InlineKeyboardButton(text="⬅ Назад", callback_data="sub:back")]
    ])

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def unsubscribed_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔔 Підписатись", callback_data="news:subscribe")],
        [InlineKeyboardButton(text="⬅ Назад", callback_data="sub:back")]
    ])


def frequency_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1 раз (🕒12:00)", callback_data="freq:1")],
        [InlineKeyboardButton(text="2 рази (🕒9:00, 🕒21:00)", callback_data="freq:2")],
        [InlineKeyboardButton(text="3 рази (🕒9:00, 🕒14:00, 🕒21:00)", callback_data="freq:3")
        ]
    ])


NEWS_TOPICS = {
    "business": "🏛️ Політика",
    "sports": "⚽ Спорт",
    "technology": "💻 Технології",
    "health": "🩺 Здоров’я",
    "entertainment": "🎉 Розваги"
}

def topics_keyboard(selected: list[str] = None):
    selected = selected or []
    buttons = []

    for topic_id, topic_name in NEWS_TOPICS.items():
        prefix = "✅ " if topic_id in selected else ""
        buttons.append(
            [InlineKeyboardButton(
                text=f"{prefix}{topic_name}",
                callback_data=f"subscription:toggle_topic:{topic_id}"
            )]
        )

    buttons.append([InlineKeyboardButton(text="✅ Готово", callback_data="subscription:topics_done")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

