from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from lang.messages import t

def idea_topic_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"🤖 {t(lang, 'topic_telegram')}", callback_data="topic:telegram"),
            InlineKeyboardButton(text=f"🕷️ {t(lang, 'topic_scraper')}", callback_data="topic:scraper"),
        ],
        [
            InlineKeyboardButton(text=f"📊 {t(lang, 'topic_analytics')}", callback_data="topic:analytics"),
            InlineKeyboardButton(text=f"🎮 {t(lang, 'topic_game')}", callback_data="topic:game"),
        ],
        [
            InlineKeyboardButton(text=f"🧰 {t(lang, 'topic_utility')}", callback_data="topic:utility"),
            InlineKeyboardButton(text=f"🧠 {t(lang, 'topic_neural')}", callback_data="topic:neural"),
        ],
    ])

def idea_difficulty_keyboard(topic: str, lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"🟢 {t(lang, 'difficulty_easy')}", callback_data=f"idea:{topic}:easy"),
            InlineKeyboardButton(text=f"🟡 {t(lang, 'difficulty_medium')}", callback_data=f"idea:{topic}:medium"),
            InlineKeyboardButton(text=f"🔴 {t(lang, 'difficulty_hard')}", callback_data=f"idea:{topic}:hard"),
        ]
    ])
