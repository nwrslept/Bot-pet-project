from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from lang.messages import t

def news_main_keyboard(lang: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "news_browse"), callback_data="news:browse")],
        [InlineKeyboardButton(text=t(lang, "news_subscribe"), callback_data="subscribe:news")]
    ])

def news_topics_keyboard(lang: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "news_topic_politics"), callback_data="news:politics")],
        [InlineKeyboardButton(text=t(lang, "news_topic_sports"), callback_data="news:sports")],
        [InlineKeyboardButton(text=t(lang, "news_topic_technology"), callback_data="news:technology")],
        [InlineKeyboardButton(text=t(lang, "news_topic_health"), callback_data="news:health")],
        [InlineKeyboardButton(text=t(lang, "news_topic_entertainment"), callback_data="news:entertainment")],
        [InlineKeyboardButton(text=t(lang, "back"), callback_data="menu:back")],
    ])

def news_action_keyboard(topic: str, lang: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "news_more"), callback_data=f"more:{topic}")],
        [InlineKeyboardButton(text=t(lang, "back"), callback_data="back:topics")],
    ])
