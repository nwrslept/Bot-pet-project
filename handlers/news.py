from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline.news import news_topics_keyboard, news_action_keyboard, news_main_keyboard
from keyboards.inline.subscription import subscription_menu_keyboard
from handlers.news_api import get_news
from keyboards.reply import main_menu_keyboard
from aiogram.types import Message

router = Router()

user_state = {}



@router.message(F.text == "📰 Новини")
async def show_news_options(message: Message):
    await message.answer("Що бажаєш зробити?", reply_markup=news_main_keyboard())


@router.callback_query(F.data == "news:browse")
async def handle_browse_news(query: CallbackQuery):
    await query.message.edit_text("Оберіть тему новин:", reply_markup=news_topics_keyboard())
    await query.answer()


@router.callback_query(F.data.startswith("news:"))
async def callback_news(query: CallbackQuery):
    topic = query.data.split(":")[1]
    user_id = query.from_user.id
    user_state[user_id] = {"topic": topic, "page": 1}

    articles, error = get_news(category=topic, page=1)
    if error:
        await query.message.edit_text(error)
        await query.answer()
        return

    article = articles[0]
    text = f"<b>{article['title']}</b>\n{article['url']}"

    await query.message.edit_text(
        text,
        reply_markup=news_action_keyboard(topic),
        parse_mode="HTML"
    )
    await query.answer()

@router.callback_query(F.data.startswith("more:"))
async def callback_more(query: CallbackQuery):
    user_id = query.from_user.id
    state = user_state.get(user_id)

    if not state:
        await query.answer("Обери тему новин спочатку.", show_alert=True)
        return

    topic = state["topic"]
    page = state["page"] + 1
    user_state[user_id]["page"] = page

    articles, error = get_news(category=topic, page=page)
    if error:
        await query.answer(error, show_alert=True)
        return

    article = articles[0]
    text = f"<b>{article['title']}</b>\n{article['url']}"

    await query.message.edit_text(
        text,
        reply_markup=news_action_keyboard(topic),
        parse_mode="HTML"
    )
    await query.answer()

@router.callback_query(F.data == "back:topics")
async def back_to_topics(query: CallbackQuery):
    await query.message.edit_text("Оберіть тему новин:", reply_markup=news_topics_keyboard())
    await query.answer()

@router.callback_query(F.data == "menu:back")
async def back_to_topics(query: CallbackQuery):
    await query.message.edit_text("Що бажаєш зробити?", reply_markup=news_main_keyboard())
    await query.answer()



