from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.db import get_connection
from database.ideas import get_user_ideas,delete_user_idea

router = Router()

@router.message(F.text == "👤 Профіль")
async def show_profile(message: Message):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (message.from_user.id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        _, telegram_id, username, first_name, last_name = user
        text = (
            f"<b>👤 Твій профіль:</b>\n\n"
            f"🆔 Telegram ID: <code>{telegram_id}</code>\n"
            f"👥 Username: @{username}\n"
            f"📛 Ім’я: {first_name or '-'}\n"
        )

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📚 Мої збережені ідеї", callback_data="show_saved_ideas")]
        ])

        await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    else:
        await message.answer("❌ Тебе немає в базі даних.")

    from aiogram.types import CallbackQuery

@router.callback_query(F.data == "show_saved_ideas")
async def show_saved_ideas(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    user_ideas = get_user_ideas(telegram_id)  # функція з твоєї БД, що повертає список ідей

    if not user_ideas:
        await callback.message.edit_text("У тебе поки немає збережених ідей.")
        await callback.answer()
        return

    # Показуємо кожну ідею з кнопкою "Видалити"
    for idea_id, topic, difficulty, idea_text in user_ideas:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Видалити", callback_data=f"delete_idea:{idea_id}")]
        ])
        text = f"💡 <b>{topic.capitalize()} ({difficulty})</b>:\n{idea_text}"
        # Надсилаємо нове повідомлення для кожної ідеї
        await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")

    await callback.answer()

@router.callback_query(F.data.startswith("delete_idea:"))
async def delete_saved_idea(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    idea_id = int(callback.data.split(":")[1])

    delete_user_idea(idea_id, telegram_id)

    await callback.answer("Ідею видалено ✅", show_alert=True)
    # Оновлюємо список ідей після видалення
    await show_saved_ideas(callback)
