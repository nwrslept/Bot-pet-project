from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline.subscription import subscription_menu_keyboard, frequency_keyboard, topics_keyboard, unsubscribed_keyboard
from database.subscriptions import update_frequency, update_topics, remove_subscription, get_user_topics

router = Router()


@router.callback_query(F.data == "subscribe:news")
async def handle_subscribe(query: CallbackQuery):
    telegram_id = query.from_user.id
    update_frequency(telegram_id, 1)

    await query.message.edit_text(
        "🔔 Меню підписки на новини",
        reply_markup=subscription_menu_keyboard()
    )
    await query.answer()

@router.callback_query(F.data == "sub:frequency")
async def choose_frequency(query: CallbackQuery):
    await query.message.edit_text("📅 Обери частоту надсилання новин:", reply_markup=frequency_keyboard())
    await query.answer()

@router.callback_query(F.data.startswith("freq:"))
async def set_frequency(query: CallbackQuery):
    frequency = int(query.data.split(":")[1])
    telegram_id = query.from_user.id
    update_frequency(telegram_id, frequency)
    await query.message.edit_text("✅ Частоту оновлено!", reply_markup=subscription_menu_keyboard())
    await query.answer()

@router.callback_query(F.data == "sub:topics")
async def choose_topics(query: CallbackQuery):
    telegram_id = query.from_user.id
    selected_topics = get_user_topics(telegram_id)  # отримуємо з бази вибрані теми
    await query.message.edit_text(
        "📰 Обери теми новин:",
        reply_markup=topics_keyboard(selected=selected_topics)
    )
    await query.answer()

@router.callback_query(F.data.startswith("subscription:toggle_topic:"))
async def toggle_topic(query: CallbackQuery):
    telegram_id = query.from_user.id
    topic_id = query.data.split(":")[-1]

    selected_topics = get_user_topics(telegram_id)
    if topic_id in selected_topics:
        selected_topics.remove(topic_id)
    else:
        selected_topics.append(topic_id)

    update_topics(telegram_id, selected_topics)
    await query.message.edit_reply_markup(reply_markup=topics_keyboard(selected=selected_topics))
    await query.answer()

@router.callback_query(F.data == "subscription:topics_done")
async def topics_done(query: CallbackQuery):
    await query.message.edit_text(
        "✅ Тема(и) збережено!",
        reply_markup=subscription_menu_keyboard()
    )
    await query.answer()


@router.callback_query(F.data == "sub:unsubscribe")
async def unsubscribe_user(query: CallbackQuery):
    telegram_id = query.from_user.id
    remove_subscription(telegram_id)
    await query.message.edit_text(
        "❌ Ви відписалися від розсилки новин.",
        reply_markup=unsubscribed_keyboard()
    )
    await query.answer()



@router.callback_query(F.data == "sub:back")
async def back_to_main(query: CallbackQuery):
    from keyboards.inline.news import news_main_keyboard
    await query.message.edit_text("Що бажаєш зробити?", reply_markup=news_main_keyboard())
    await query.answer()
