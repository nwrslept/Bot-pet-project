from aiogram import Router, F
from aiogram.types import Message
from database.db import get_connection

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
    else:
        text = "❌ Тебе немає в базі даних."

    await message.answer(text, parse_mode="HTML")
