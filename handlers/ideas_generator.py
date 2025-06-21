from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
import os
from dotenv import load_dotenv
import google.generativeai as genai
from keyboards.inline.ideas import idea_difficulty_keyboard

# 🧠 Імпортуємо збереження / отримання ідей
from database.ideas import save_idea, get_ideas_by_difficulty

router = Router()

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash-latest")

@router.message(F.text == "💡 Згенерувати ідею")
async def choose_difficulty(message: Message):
    await message.answer(
        "Оберіть складність ідеї:",
        reply_markup=idea_difficulty_keyboard()
    )

@router.callback_query(F.data.startswith("idea:"))
async def generate_idea_by_difficulty(callback: CallbackQuery):
    difficulty = callback.data.split(":")[1]

    # 🧠 Отримуємо попередні ідеї
    previous_ideas = get_ideas_by_difficulty(difficulty)
    context = "\n".join(f"- {idea}" for idea in previous_ideas)

    # 📝 Промпт із урахуванням історії
    prompt = f"""
Ти — генератор унікальних ідей для скриптів на Python рівня {difficulty}.
Ось попередні ідеї, які вже були:

{context if context else '(Ще немає попередніх ідей)'}

Згенеруй одну нову ідею, яка суттєво відрізняється від усіх попередніх.
Напиши лише короткий опис скрипта, без коду і зайвих пояснень.
"""

    try:
        await callback.message.edit_text("🔄 Генеруємо ідею...")
        await callback.bot.send_chat_action(chat_id=callback.message.chat.id, action="typing")

        response = model.generate_content(prompt)
        idea = response.text.strip()

        # 💾 Зберігаємо у БД
        save_idea(difficulty, idea)

        await callback.message.edit_text(f"💡 Ідея ({difficulty}):\n{idea}")
        await callback.answer()
    except Exception as e:
        await callback.message.edit_text(f"⚠ Помилка при генерації ідеї:\n{e}")
