from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from lang.messages import t

def subscription_menu_keyboard(lang: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "frequency_btn"), callback_data="sub:frequency")],
        [InlineKeyboardButton(text=t(lang, "topics_btn"), callback_data="sub:topics")],
        [InlineKeyboardButton(text=t(lang, "unsubscribe_btn"), callback_data="sub:unsubscribe")],
        [InlineKeyboardButton(text=t(lang, "back_btn"), callback_data="sub:back")]
    ])

def unsubscribed_keyboard(lang: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "subscribe_btn"), callback_data="news:subscribe")],
        [InlineKeyboardButton(text=t(lang, "back_btn"), callback_data="sub:back")]
    ])

def frequency_keyboard(lang: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "freq_once"), callback_data="freq:1")],
        [InlineKeyboardButton(text=t(lang, "freq_twice"), callback_data="freq:2")],
        [InlineKeyboardButton(text=t(lang, "freq_thrice"), callback_data="freq:3")]
    ])

NEWS_TOPICS = {
    "business": "politics",
    "sports": "sports",
    "technology": "technology",
    "health": "health",
    "entertainment": "entertainment"
}

def topics_keyboard(lang: str, selected: list[str] = None):
    selected = selected or []
    buttons = []

    for topic_id in NEWS_TOPICS:
        prefix = "✅ " if topic_id in selected else ""
        # переклад назв тем
        topic_name = t(lang, f"topic_{topic_id}")
        buttons.append(
            [InlineKeyboardButton(
                text=f"{prefix}{topic_name}",
                callback_data=f"subscription:toggle_topic:{topic_id}"
            )]
        )

    buttons.append([InlineKeyboardButton(text=t(lang, "done_btn"), callback_data="subscription:topics_done")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
