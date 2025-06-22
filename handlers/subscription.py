from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline.subscription import subscription_menu_keyboard, frequency_keyboard, topics_keyboard, unsubscribed_keyboard
from database.subscriptions import update_frequency, update_topics, remove_subscription, get_user_topics
from lang.messages import t, get_user_language

router = Router()

@router.callback_query(F.data == "subscribe:news")
async def handle_subscribe(query: CallbackQuery):
    telegram_id = query.from_user.id
    lang = get_user_language(telegram_id)
    update_frequency(telegram_id, 1)

    await query.message.edit_text(
        t(lang, "subscription_menu"),
        reply_markup=subscription_menu_keyboard(lang)
    )
    await query.answer()

@router.callback_query(F.data == "sub:frequency")
async def choose_frequency(query: CallbackQuery):
    lang = get_user_language(query.from_user.id)
    await query.message.edit_text(
        t(lang, "choose_frequency"),
        reply_markup=frequency_keyboard(lang)
    )
    await query.answer()

@router.callback_query(F.data.startswith("freq:"))
async def set_frequency(query: CallbackQuery):
    frequency = int(query.data.split(":")[1])
    telegram_id = query.from_user.id
    lang = get_user_language(telegram_id)
    update_frequency(telegram_id, frequency)
    await query.message.edit_text(
        t(lang, "frequency_updated"),
        reply_markup=subscription_menu_keyboard(lang)
    )
    await query.answer()

@router.callback_query(F.data == "sub:topics")
async def choose_topics(query: CallbackQuery):
    telegram_id = query.from_user.id
    lang = get_user_language(telegram_id)
    selected_topics = get_user_topics(telegram_id)
    await query.message.edit_text(
        t(lang, "choose_topics"),
        reply_markup=topics_keyboard(lang, selected=selected_topics)
    )
    await query.answer()

@router.callback_query(F.data.startswith("subscription:toggle_topic:"))
async def toggle_topic(query: CallbackQuery):
    telegram_id = query.from_user.id
    lang = get_user_language(telegram_id)
    topic_id = query.data.split(":")[-1]

    selected_topics = get_user_topics(telegram_id)
    if topic_id in selected_topics:
        selected_topics.remove(topic_id)
    else:
        selected_topics.append(topic_id)

    update_topics(telegram_id, selected_topics)
    await query.message.edit_reply_markup(reply_markup=topics_keyboard(lang, selected=selected_topics))
    await query.answer()

@router.callback_query(F.data == "subscription:topics_done")
async def topics_done(query: CallbackQuery):
    lang = get_user_language(query.from_user.id)
    await query.message.edit_text(
        t(lang, "topics_saved"),
        reply_markup=subscription_menu_keyboard(lang)
    )
    await query.answer()

@router.callback_query(F.data == "sub:unsubscribe")
async def unsubscribe_user(query: CallbackQuery):
    telegram_id = query.from_user.id
    lang = get_user_language(telegram_id)
    remove_subscription(telegram_id)
    await query.message.edit_text(
        t(lang, "unsubscribed"),
        reply_markup=unsubscribed_keyboard(lang)
    )
    await query.answer()

@router.callback_query(F.data == "sub:back")
async def back_to_main(query: CallbackQuery):
    from keyboards.inline.news import news_main_keyboard
    lang = get_user_language(query.from_user.id)
    await query.message.edit_text(
        t(lang, "what_to_do"),
        reply_markup=news_main_keyboard(lang)
    )
    await query.answer()
