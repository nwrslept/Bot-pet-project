from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from keyboards.reply import main_menu_keyboard
from database.db import get_connection

router = Router()

@router.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    conn = get_connection()
    cursor = conn.cursor()
    user_name = message.from_user.first_name
    cursor.execute("""
            INSERT OR IGNORE INTO users (telegram_id, username, first_name, last_name)
            VALUES (?, ?, ?, ?)
        """, (message.from_user.id, message.from_user.username, message.from_user.first_name,
              message.from_user.last_name))

    conn.commit()
    conn.close()

    photo = FSInputFile("images/welcome.png")

    caption = (
        f"<b>Вітаю, {user_name}!</b>\n\n"
        "Це мій невеличкий пет-проєкт — 🛠️ Telegram-бот-помічник, "
        "який допоможе зробити твої повсякденні справи простішими та приємнішими 😌\n\n"
        "Вибери дію з меню нижче 👇"
    )

    await message.answer_photo(photo=photo, caption=caption, reply_markup=main_menu_keyboard(), parse_mode="HTML")
