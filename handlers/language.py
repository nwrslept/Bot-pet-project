from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.inline.language import language_keyboard
from database.db import get_connection
from keyboards.reply import main_menu_keyboard
from lang.messages import t

router = Router()

@router.message(F.text.in_({"🌍 Мова", "🌍 Language"}))
async def ask_language_user(message: Message):
    await message.answer(
        "🌐 Оберіть мову / Choose language:",
        reply_markup=language_keyboard()
    )



@router.callback_query(F.data.startswith("lang:"))
async def set_language(callback: CallbackQuery):
    lang = callback.data.split(":")[1]
    telegram_id = callback.from_user.id

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET language = ? WHERE telegram_id = ?", (lang, telegram_id))
    conn.commit()
    conn.close()

    text = t(lang, "choosed_language")

    # Відповідаємо новим повідомленням з ReplyKeyboardMarkup
    await callback.message.answer(
        f"✅ {text}",
        reply_markup=main_menu_keyboard(lang)
    )
    # Видаляємо старе повідомлення (за бажанням)
    await callback.message.delete()

    await callback.answer()
