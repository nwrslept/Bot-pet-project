from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.db import get_connection
from database.ideas import get_user_ideas, delete_user_idea
from lang.messages import t, get_user_language  # <-- імпортуємо переклад

router = Router()


@router.message(F.text.in_({"👤 Профіль", "👤 Profile"}))
async def show_profile(message: Message):
    lang = get_user_language(message.from_user.id)  # отримуємо мову користувача

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT telegram_id, username, first_name, last_name FROM users WHERE telegram_id = ?",
        (message.from_user.id,)
    )
    user = cursor.fetchone()

    if user:
        telegram_id, username, first_name, last_name = user
        text = (
            f"<b>{t(lang, 'profile_title')}</b>\n\n"
            f"{t(lang, 'profile_id')}: <code>{telegram_id}</code>\n"
            f"{t(lang, 'profile_username')}: @{username}\n"
            f"{t(lang, 'profile_first_name')}: {first_name or '-'}\n"
        )

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "button_saved_ideas"), callback_data="show_saved_ideas")]
        ])

        await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    else:
        await message.answer(t(lang, "profile_not_found"))


@router.callback_query(F.data == "show_saved_ideas")
async def show_saved_ideas(callback: CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    telegram_id = callback.from_user.id
    user_ideas = get_user_ideas(telegram_id)

    if not user_ideas:
        await callback.message.edit_text(t(lang, "no_ideas"))
        await callback.answer()
        return

    for idea_id, topic, difficulty, idea_text in user_ideas:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "button_delete"), callback_data=f"delete_idea:{idea_id}")]
        ])
        text = f"💡 <b>{topic.capitalize()} ({difficulty})</b>:\n{idea_text}"
        await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")

    await callback.answer()


@router.callback_query(F.data.startswith("delete_idea:"))
async def delete_saved_idea(callback: CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    telegram_id = callback.from_user.id
    idea_id = int(callback.data.split(":")[1])

    delete_user_idea(idea_id, telegram_id)

    await callback.answer(t(lang, "idea_deleted"), show_alert=True)
    await show_saved_ideas(callback)
