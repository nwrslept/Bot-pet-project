from aiogram import Router
from aiogram.filters import Command
from keyboards.reply import main_menu_keyboard
from database.db import get_connection
from aiogram.types import Message, FSInputFile
from keyboards.inline.language import language_keyboard
from lang.messages import get_user_language, t

router = Router()

@router.message(Command(commands=["start"]))
async def cmd_start(message: Message):


    conn = get_connection()
    cursor = conn.cursor()
    telegram_id = message.from_user.id
    user_name = message.from_user.first_name

    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    user_exists = cursor.fetchone()

    if not user_exists:
        cursor.execute("""
            INSERT INTO users (telegram_id, username, first_name, last_name, language)
            VALUES (?, ?, ?, ?, ?)
        """, (
            telegram_id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
            'uk'
        ))
        conn.commit()
        conn.close()

        await message.answer("🌍 Обери мову / Choose your language:", reply_markup=language_keyboard())
        return

    conn.close()

    lang = get_user_language(telegram_id)

    photo = FSInputFile("images/welcome.png")
    caption = (
        f"<b>{t(lang,"start1", user=user_name)}!</b>\n\n"
        f"{t(lang, "start2")}\n\n"
        f"{t(lang, "start3")}"
    )

    await message.answer_photo(photo=photo, caption=caption, reply_markup=main_menu_keyboard(lang), parse_mode="HTML")
